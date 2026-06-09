"""
exams/services.py
Auto-mark MCQ, manual written marks, and teacher finalisation.
"""
from decimal import Decimal

from django.utils import timezone

from academics.models import ClassEnrollment
from notifications.services import notify_user

from .models import Exam, ExamAnswer, ExamQuestion, ExamResult


def ensure_results_for_exam(exam):
    """Create empty result rows for every student enrolled in the exam class."""
    enrolled = ClassEnrollment.objects.filter(class_group=exam.class_group).select_related('student')
    for enr in enrolled:
        ExamResult.objects.get_or_create(exam=exam, student=enr.student)


def auto_mark_mcq(result):
    """Score all MCQ answers and store auto_score on the result."""
    total = Decimal('0')
    for answer in result.answers.select_related('question'):
        q = answer.question
        if q.question_type != ExamQuestion.TYPE_MCQ:
            continue
        if answer.selected_option and answer.selected_option == q.correct_option:
            answer.marks_awarded = Decimal(q.max_marks)
            answer.is_auto_marked = True
        else:
            answer.marks_awarded = Decimal('0')
            answer.is_auto_marked = True
        answer.save(update_fields=['marks_awarded', 'is_auto_marked'])
        total += answer.marks_awarded or Decimal('0')
    result.auto_score = total
    result.save(update_fields=['auto_score'])
    _recalculate_final_score(result)
    return result


def apply_manual_marks(result, marks_by_question_id):
    """Teacher awards marks for written questions."""
    manual_total = Decimal('0')
    for qid, marks in marks_by_question_id.items():
        try:
            answer = result.answers.get(question_id=int(qid))
            q = answer.question
            if q.question_type != ExamQuestion.TYPE_WRITTEN:
                continue
            awarded = Decimal(str(marks))
            if awarded > q.max_marks:
                awarded = Decimal(q.max_marks)
            answer.marks_awarded = awarded
            answer.is_auto_marked = False
            answer.save(update_fields=['marks_awarded', 'is_auto_marked'])
            manual_total += awarded
        except ExamAnswer.DoesNotExist:
            continue
    result.manual_score = manual_total
    result.status = ExamResult.STATUS_MARKED
    result.save(update_fields=['manual_score', 'status'])
    _recalculate_final_score(result)
    return result


def _recalculate_final_score(result):
    auto = result.auto_score or Decimal('0')
    manual = result.manual_score or Decimal('0')
    result.final_score = auto + manual
    result.save(update_fields=['final_score'])


def finalise_result(*, result, teacher_profile, comment=''):
    exam = result.exam
    if exam.teacher_id != teacher_profile.id:
        raise PermissionError('Only the exam teacher can finalise results.')
    if result.status not in (ExamResult.STATUS_MARKED, ExamResult.STATUS_DRAFT):
        raise ValueError('Result cannot be finalised in its current state.')
    if result.final_score is None:
        _recalculate_final_score(result)

    result.status = ExamResult.STATUS_FINALISED
    result.teacher_comment = comment
    result.signed_off_by = teacher_profile
    result.signed_off_at = timezone.now()
    result.save(update_fields=[
        'status', 'teacher_comment', 'signed_off_by', 'signed_off_at', 'final_score',
    ])

    if result.student.user_id:
        notify_user(
            user=result.student.user,
            school=exam.school,
            notification_type='exam',
            title='Exam results finalised',
            message=f'{exam.title}: {result.final_score} marks',
            link_path=f'/exams/{exam.pk}/',
        )
    return result


def save_student_answers(result, answers_data):
    """Persist student answers and auto-mark MCQ."""
    for q in result.exam.questions.all():
        data = answers_data.get(str(q.pk), {})
        answer, _ = ExamAnswer.objects.get_or_create(result=result, question=q)
        if q.question_type == ExamQuestion.TYPE_MCQ:
            answer.selected_option = data.get('selected_option', '')
        else:
            answer.written_answer = data.get('written_answer', '')
        answer.save()
    result.submitted_at = timezone.now()
    result.status = ExamResult.STATUS_MARKED
    result.save(update_fields=['submitted_at', 'status'])
    auto_mark_mcq(result)
    return result


def publish_exam(exam):
    exam.status = Exam.STATUS_PUBLISHED
    exam.save(update_fields=['status'])
    ensure_results_for_exam(exam)
    return exam

"""exams/views.py — exam builder, marking, and finalisation."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pages.decorators import role_required
from pages.enrollment_service import student_profile_for_user
from pages.portal import build_portal_context
from parents.models import StudentParentLink

from .forms import ExamForm, ExamQuestionForm, StudentExamForm
from .models import Exam, ExamQuestion, ExamResult
from .services import (
    apply_manual_marks,
    ensure_results_for_exam,
    finalise_result,
    publish_exam,
    save_student_answers,
)


def _ctx(request, title, meta=''):
    return build_portal_context(request, title, meta)


def _exams_for_user(user):
    if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
        return Exam.objects.filter(teacher=user.teacher_profile).select_related(
            'class_group', 'subject',
        )
    if user.role == 'student' and hasattr(user, 'student_profile'):
        return Exam.objects.filter(
            status=Exam.STATUS_PUBLISHED,
            class_group__enrollments__student=user.student_profile,
        ).distinct().select_related('class_group', 'subject')
    if user.role == 'parent' and hasattr(user, 'parent_profile'):
        child_ids = StudentParentLink.objects.filter(
            parent=user.parent_profile,
        ).values_list('student_id', flat=True)
        return Exam.objects.filter(
            status=Exam.STATUS_PUBLISHED,
            class_group__enrollments__student_id__in=child_ids,
        ).distinct().select_related('class_group', 'subject')
    if user.role == 'school_admin' and user.school_id:
        return Exam.objects.filter(school=user.school).select_related('class_group', 'subject')
    return Exam.objects.none()


def _results_visible_to_role(user, exam):
    """Parents and students only see finalised results."""
    qs = exam.results.select_related('student', 'signed_off_by')
    if user.role == 'student' and hasattr(user, 'student_profile'):
        return qs.filter(
            student=user.student_profile,
            status=ExamResult.STATUS_FINALISED,
        )
    if user.role == 'parent' and hasattr(user, 'parent_profile'):
        child_ids = StudentParentLink.objects.filter(
            parent=user.parent_profile,
        ).values_list('student_id', flat=True)
        return qs.filter(
            student_id__in=child_ids,
            status=ExamResult.STATUS_FINALISED,
        )
    return qs


@login_required
def exams_list(request):
    exams = _exams_for_user(request.user)
    ctx = _ctx(request, 'Exams', 'MCQ auto-mark + written; results official only when finalised.')
    ctx['exams'] = exams
    ctx['can_create'] = request.user.role == 'teacher'
    return render(request, 'exams/list.html', ctx)


@role_required('teacher')
def exam_create(request):
    teacher = request.user.teacher_profile
    if request.method == 'POST':
        form = ExamForm(request.user.school, request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.school = request.user.school
            exam.teacher = teacher
            exam.save()
            messages.success(request, f'Exam "{exam.title}" created.')
            return redirect('exams:detail', exam_id=exam.pk)
    else:
        form = ExamForm(request.user.school)
    ctx = _ctx(request, 'New exam', 'Create an exam paper for a class.')
    ctx['form'] = form
    return render(request, 'exams/exam_form.html', ctx)


@login_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(
        Exam.objects.select_related('class_group', 'subject', 'teacher').prefetch_related('questions'),
        pk=exam_id,
    )
    user = request.user
    allowed = False
    if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
        allowed = exam.teacher_id == user.teacher_profile.id
    elif user.role == 'student' and hasattr(user, 'student_profile'):
        allowed = (
            exam.status == Exam.STATUS_PUBLISHED
            and exam.class_group.enrollments.filter(student=user.student_profile).exists()
        )
    elif user.role == 'parent' and hasattr(user, 'parent_profile'):
        child_ids = StudentParentLink.objects.filter(parent=user.parent_profile).values_list(
            'student_id', flat=True,
        )
        allowed = (
            exam.status == Exam.STATUS_PUBLISHED
            and exam.class_group.enrollments.filter(student_id__in=child_ids).exists()
        )
    elif user.role == 'school_admin':
        allowed = exam.school_id == user.school_id
    if not allowed:
        return redirect('pages:dashboard')

    is_teacher = user.role == 'teacher' and exam.teacher_id == user.teacher_profile.id
    student_result = None
    student_form = None

    if user.role == 'student':
        student_result, _ = ExamResult.objects.get_or_create(
            exam=exam, student=user.student_profile,
        )
        if exam.status == Exam.STATUS_PUBLISHED and student_result.status != ExamResult.STATUS_FINALISED:
            student_form = StudentExamForm(exam)
            if request.method == 'POST':
                student_form = StudentExamForm(exam, request.POST)
                if student_form.is_valid():
                    answers = {}
                    for q in exam.questions.all():
                        key = f'q_{q.pk}'
                        val = student_form.cleaned_data.get(key, '')
                        if q.question_type == ExamQuestion.TYPE_MCQ:
                            answers[str(q.pk)] = {'selected_option': val}
                        else:
                            answers[str(q.pk)] = {'written_answer': val}
                    save_student_answers(student_result, answers)
                    messages.success(request, 'Answers submitted — MCQ auto-marked.')
                    return redirect('exams:detail', exam_id=exam.pk)

    results = _results_visible_to_role(user, exam)
    if is_teacher and exam.status == Exam.STATUS_DRAFT:
        ensure_results_for_exam(exam)

    question_form = ExamQuestionForm() if is_teacher else None
    ctx = _ctx(request, exam.title, exam.subject.name)
    ctx.update({
        'exam': exam,
        'questions': exam.questions.all(),
        'results': results,
        'question_form': question_form,
        'student_result': student_result,
        'student_form': student_form,
        'is_teacher': is_teacher,
        'show_build': is_teacher,
        'show_finalise': is_teacher,
    })
    return render(request, 'exams/detail.html', ctx)


@role_required('teacher')
@require_POST
def exam_add_question(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user.teacher_profile)
    form = ExamQuestionForm(request.POST)
    if form.is_valid():
        q = form.save(commit=False)
        q.exam = exam
        q.save()
        messages.success(request, 'Question added.')
    else:
        messages.error(request, 'Could not add question.')
    return redirect('exams:detail', exam_id=exam.pk)


@role_required('teacher')
@require_POST
def exam_publish(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user.teacher_profile)
    if not exam.questions.exists():
        messages.error(request, 'Add at least one question before publishing.')
        return redirect('exams:detail', exam_id=exam.pk)
    publish_exam(exam)
    messages.success(request, 'Exam published — students can now sit it.')
    return redirect('exams:detail', exam_id=exam.pk)


@role_required('teacher')
@require_POST
def exam_mark_written(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user.teacher_profile)
    result_id = request.POST.get('result_id')
    result = get_object_or_404(ExamResult, pk=result_id, exam=exam)
    marks = {}
    for key, val in request.POST.items():
        if key.startswith('marks_'):
            qid = key.replace('marks_', '')
            marks[qid] = val
    apply_manual_marks(result, marks)
    messages.success(request, f'Manual marks saved for {result.student.full_name}.')
    return redirect('exams:detail', exam_id=exam.pk)


@role_required('teacher')
@require_POST
def exam_finalise(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id, teacher=request.user.teacher_profile)
    result_id = request.POST.get('result_id')
    comment = request.POST.get('comment', '')
    result = get_object_or_404(ExamResult, pk=result_id, exam=exam)
    try:
        finalise_result(
            result=result,
            teacher_profile=request.user.teacher_profile,
            comment=comment,
        )
        messages.success(request, f'Results finalised for {result.student.full_name}.')
    except (PermissionError, ValueError) as exc:
        messages.error(request, str(exc))
    return redirect('exams:detail', exam_id=exam.pk)

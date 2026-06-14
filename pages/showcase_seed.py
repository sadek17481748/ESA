"""
One fully-populated student + parent pair for screenshots and assessor walkthroughs.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

from academics.models import BehaviourRecord, ClassEnrollment, ClassGroup
from attendance.models import AttendanceMark
from exams.models import Exam, ExamQuestion, ExamResult
from exams.services import (
    apply_manual_marks,
    auto_mark_mcq,
    ensure_results_for_exam,
    finalise_result,
    publish_exam,
    save_student_answers,
)
from homework.models import Assignment, Submission
from homework.services import sign_off_submission
from hifz.models import HifzJuzSignOff
from hifz.services import sign_off_hifz_juz
from lms.models import (
    ClassTrackAssignment,
    CourseMaterial,
    CourseSubject,
    CourseTrack,
    MaterialSubmission,
    StudentMaterialProgress,
)
from messaging.models import (
    SchoolConversation,
    SchoolMessage,
    SupportCase,
    SupportMessage,
    TeacherReport,
)
from notifications.models import Notification
from notifications.services import notify_user
from parents.models import ParentProfile, StudentParentLink
from payments.models import FeeItem
from quran.models import QuranSession
from quran.services import mark_session_reviewed, save_page_markup
from students.models import StudentProfile
from teachers.models import TeacherProfile

from pages.attendance_service import get_or_create_session
from pages.seed_helpers import upsert_user

User = get_user_model()

SHOWCASE_STUDENT_USERNAME = 'demo_student'
SHOWCASE_PARENT_USERNAME = 'demo_parent'
SHOWCASE_PASSWORD = 'Demo2026!'
SHOWCASE_ADMISSION = 'DEMO-001'
SHOWCASE_CLASS = '7A'


def seed_showcase_account(school, *, stdout=None):
    """Create demo_student / demo_parent with attendance, reports, fees, and more."""
    write = stdout.write if stdout else (lambda msg: None)

    class_group = ClassGroup.objects.filter(school=school, name=SHOWCASE_CLASS).first()
    if not class_group:
        raise ValueError(f'Class {SHOWCASE_CLASS} not found — run seed_alnoor_full_school first.')

    teacher_user = User.objects.filter(username='mr_mohammed', school=school).first()
    teacher_profile = (
        TeacherProfile.objects.filter(user=teacher_user).first() if teacher_user else None
    )
    school_admin = User.objects.filter(username='schooladmin', school=school).first()
    super_user = User.objects.filter(username='super', role='super_admin').first()

    parent_user, _ = upsert_user(
        SHOWCASE_PARENT_USERNAME,
        email='fatima.hassan.demo@alnoor.example',
        role='parent',
        password=SHOWCASE_PASSWORD,
        school=school,
        first_name='Fatima',
        last_name='Hassan',
        force_reset_password=True,
    )
    parent_profile, _ = ParentProfile.objects.get_or_create(
        user=parent_user,
        defaults={'school': school},
    )

    student_user, _ = upsert_user(
        SHOWCASE_STUDENT_USERNAME,
        email='amina.hassan.demo@alnoor.example',
        role='student',
        password=SHOWCASE_PASSWORD,
        school=school,
        first_name='Amina',
        last_name='Hassan',
        force_reset_password=True,
    )
    student_profile, _ = StudentProfile.objects.get_or_create(
        user=student_user,
        defaults={
            'school': school,
            'first_name': 'Amina',
            'last_name': 'Hassan',
            'year_group': 'Year 7',
            'admission_number': SHOWCASE_ADMISSION,
        },
    )
    student_profile.school = school
    student_profile.first_name = 'Amina'
    student_profile.last_name = 'Hassan'
    student_profile.year_group = 'Year 7'
    student_profile.admission_number = SHOWCASE_ADMISSION
    student_profile.is_active = True
    student_profile.save()

    StudentParentLink.objects.get_or_create(
        parent=parent_profile,
        student=student_profile,
        defaults={'relationship': 'mother'},
    )
    ClassEnrollment.objects.get_or_create(
        class_group=class_group,
        student=student_profile,
    )

    _seed_attendance(school, class_group, student_profile, write)
    _seed_behaviour(school, student_profile, teacher_user, write)
    _seed_homework(school, class_group, student_profile, teacher_profile, write)
    _seed_exam(school, class_group, student_profile, teacher_profile, write)
    _seed_quran(school, student_profile, teacher_profile, write)
    _seed_hifz(school, student_profile, teacher_user, write)
    _seed_messaging(school, parent_user, student_profile, teacher_user, school_admin, super_user, write)
    _seed_fees(school, parent_user, student_profile, write)
    _seed_lms(school, class_group, student_profile, teacher_user, write)
    _seed_notifications(school, parent_user, student_user, student_profile, write)

    write('  showcase account ready')
    return parent_user, student_user, student_profile


def _seed_attendance(school, class_group, student, write):
    today = date.today()
    marks = (
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_LATE,
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_ABSENT,
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_PRESENT,
    )
    for day_offset, status in enumerate(marks):
        session_date = today - timedelta(days=day_offset)
        session = get_or_create_session(school, class_group, session_date, None)
        AttendanceMark.objects.update_or_create(
            session=session,
            student=student,
            defaults={
                'status': status,
                'note': 'Approved late pass' if status == AttendanceMark.STATUS_LATE else '',
            },
        )
    write('    attendance: 7 days marked')


def _seed_behaviour(school, student, teacher_user, write):
    if not teacher_user:
        return
    BehaviourRecord.objects.get_or_create(
        school=school,
        student=student,
        title='Star pupil — Quran lesson',
        defaults={
            'teacher': teacher_user,
            'record_type': BehaviourRecord.TYPE_COMMENDATION,
            'notes': 'Excellent tajweed and focus during memorisation.',
        },
    )
    BehaviourRecord.objects.get_or_create(
        school=school,
        student=student,
        title='Late to morning registration',
        defaults={
            'teacher': teacher_user,
            'record_type': BehaviourRecord.TYPE_INCIDENT,
            'notes': 'Arrived 8 minutes late — parent informed.',
        },
    )
    write('    behaviour: commendation + incident')


def _seed_homework(school, class_group, student, teacher_profile, write):
    if not teacher_profile:
        return
    from subjects.models import Subject

    maths = Subject.objects.filter(school=school, name='Maths').first()
    if not maths:
        return

    today = date.today()
    hw, _ = Assignment.objects.get_or_create(
        school=school,
        class_group=class_group,
        title='Showcase maths homework — 7A',
        defaults={
            'subject': maths,
            'teacher': teacher_profile,
            'description': 'Complete exercises 1–10. Show full working.',
            'assignment_type': Assignment.TYPE_HOMEWORK,
            'due_date': today + timedelta(days=5),
        },
    )
    sub, _ = Submission.objects.get_or_create(
        assignment=hw,
        student=student,
        defaults={
            'body': 'Amina completed all questions with clear working shown.',
            'status': Submission.STATUS_SUBMITTED,
            'submitted_at': timezone.now() - timedelta(days=1),
        },
    )
    if sub.status == Submission.STATUS_SUBMITTED:
        try:
            sign_off_submission(
                submission=sub,
                teacher_profile=teacher_profile,
                approve=True,
                note='Excellent work — well done Amina!',
            )
        except (PermissionError, ValueError):
            pass
    write('    homework: signed-off submission')


def _seed_exam(school, class_group, student, teacher_profile, write):
    if not teacher_profile:
        return
    from subjects.models import Subject

    maths = Subject.objects.filter(school=school, name='Maths').first()
    if not maths:
        return

    exam, created = Exam.objects.get_or_create(
        school=school,
        class_group=class_group,
        title='Showcase maths assessment — Amina Hassan',
        defaults={
            'subject': maths,
            'teacher': teacher_profile,
            'exam_date': date.today() - timedelta(days=10),
            'status': Exam.STATUS_DRAFT,
        },
    )
    if created or not exam.questions.exists():
        ExamQuestion.objects.get_or_create(
            exam=exam,
            sort_order=0,
            defaults={
                'question_type': ExamQuestion.TYPE_MCQ,
                'prompt': 'What is 2/5 + 1/5?',
                'option_a': '3/5',
                'option_b': '3/10',
                'option_c': '1/5',
                'option_d': '2/5',
                'correct_option': 'a',
                'max_marks': 2,
            },
        )
        ExamQuestion.objects.get_or_create(
            exam=exam,
            sort_order=1,
            defaults={
                'question_type': ExamQuestion.TYPE_WRITTEN,
                'prompt': 'Show how to simplify 12/18.',
                'max_marks': 4,
            },
        )

    publish_exam(exam)
    ensure_results_for_exam(exam)
    result, _ = ExamResult.objects.get_or_create(exam=exam, student=student)
    mcq = exam.questions.filter(question_type=ExamQuestion.TYPE_MCQ).first()
    written = exam.questions.filter(question_type=ExamQuestion.TYPE_WRITTEN).first()
    answers = {}
    if mcq:
        answers[str(mcq.pk)] = {'selected_option': 'a'}
    if written:
        answers[str(written.pk)] = {'written_answer': 'Divide top and bottom by 6 → 2/3.'}
    save_student_answers(result, answers)
    if written:
        apply_manual_marks(result, {str(written.pk): 4})
    auto_mark_mcq(result)
    try:
        finalise_result(
            result=result,
            teacher_profile=teacher_profile,
            comment='Strong understanding of fractions — well done.',
        )
    except (PermissionError, ValueError):
        pass
    write('    exam: finalised result')


def _seed_quran(school, student, teacher_profile, write):
    if not teacher_profile:
        return
    session, _ = QuranSession.objects.get_or_create(
        school=school,
        student=student,
        teacher=teacher_profile,
        surah_name='Mushaf',
        defaults={'status': QuranSession.STATUS_SUBMITTED},
    )
    save_page_markup(
        session=session,
        para_number=1,
        page_number=2,
        note='Strong memorisation — work on elongation (madd).',
        highlights=[{'x': 0.2, 'y': 0.3, 'w': 0.35, 'h': 0.04, 'color': '#fff59d'}],
    )
    try:
        mark_session_reviewed(
            session,
            teacher_profile,
            notes='Recitation reviewed — continue daily muraja’ah.',
        )
    except (PermissionError, ValueError):
        pass
    write('    quran: session with notes and highlights')


def _seed_hifz(school, student, teacher_user, write):
    if not teacher_user:
        return
    for juz in (1, 2, 3):
        if HifzJuzSignOff.objects.filter(student=student, juz_number=juz).exists():
            continue
        try:
            sign_off_hifz_juz(
                student=student,
                juz_number=juz,
                teacher_user=teacher_user,
            )
        except ValueError:
            pass
    write('    hifz: juz 1–3 signed off (parent messages sent)')


def _seed_messaging(school, parent_user, student, teacher_user, school_admin, super_user, write):
    if teacher_user:
        conv, created = SchoolConversation.objects.get_or_create(
            school=school,
            subject=f'Progress update — {student.full_name}',
            created_by=teacher_user,
            recipient_type=SchoolConversation.RECIPIENT_PARENT,
            recipient_user=parent_user,
            defaults={'created_by': teacher_user},
        )
        if created or conv.messages.count() < 2:
            SchoolMessage.objects.get_or_create(
                conversation=conv,
                sender=teacher_user,
                defaults={
                    'body': (
                        f'As-salamu alaykum — {student.first_name} is making excellent '
                        'progress in Quran and maths this term.'
                    ),
                },
            )
            SchoolMessage.objects.get_or_create(
                conversation=conv,
                sender=parent_user,
                defaults={'body': 'JazakAllah khayr for the update — we are very proud.'},
            )

        TeacherReport.objects.get_or_create(
            school=school,
            student=student,
            subject_line=f'Spring term report — {student.full_name}',
            defaults={
                'teacher': teacher_user,
                'parent': parent_user,
                'period_covered': 'Spring term 2026',
                'strengths': 'Attentive in lessons, homework always on time, strong Quran recitation.',
                'areas_for_improvement': 'Continue daily times-table practice (6–12).',
                'action_required': 'Sign the reading log each week.',
                'additional_notes': 'Parents evening: Thursday 4pm — all welcome.',
            },
        )

    if school_admin:
        conv_office, created = SchoolConversation.objects.get_or_create(
            school=school,
            subject='After-school club — Amina Hassan',
            created_by=parent_user,
            recipient_type=SchoolConversation.RECIPIENT_SCHOOL,
            defaults={'created_by': parent_user},
        )
        if created or conv_office.messages.count() < 2:
            SchoolMessage.objects.get_or_create(
                conversation=conv_office,
                sender=parent_user,
                defaults={'body': 'Please confirm Amina is registered for Saturday Arabic club.'},
            )
            SchoolMessage.objects.get_or_create(
                conversation=conv_office,
                sender=school_admin,
                defaults={
                    'body': 'Confirmed — Amina is on the register. First session Saturday 10am.',
                },
            )

    if super_user:
        case, _ = SupportCase.objects.get_or_create(
            case_number='ESA-DEMO01',
            defaults={
                'opened_by': parent_user,
                'subject': 'Question about attendance notifications',
                'status': SupportCase.STATUS_OPEN,
            },
        )
        SupportMessage.objects.get_or_create(
            case=case,
            sender=parent_user,
            defaults={
                'body': 'Will I receive an email when attendance is marked for Amina?',
            },
        )
        SupportMessage.objects.get_or_create(
            case=case,
            sender=super_user,
            defaults={
                'body': 'Yes — enable email notifications under Messages → preferences.',
                'is_staff_reply': True,
            },
        )

    write('    messaging: conversations, teacher report, support case')


def _seed_fees(school, parent_user, student, write):
    today = date.today()
    FeeItem.objects.get_or_create(
        school=school,
        parent=parent_user,
        title=f'Term 3 tuition — {student.admission_number}',
        defaults={
            'child_name': student.full_name,
            'description': 'Spring term tuition fees',
            'amount_pence': 25000,
            'due_date': today + timedelta(days=14),
            'status': FeeItem.STATUS_OUTSTANDING,
        },
    )
    FeeItem.objects.get_or_create(
        school=school,
        parent=parent_user,
        title=f'Term 2 tuition — {student.admission_number}',
        defaults={
            'child_name': student.full_name,
            'description': 'Paid last term',
            'amount_pence': 25000,
            'due_date': today - timedelta(days=60),
            'status': FeeItem.STATUS_PAID,
        },
    )
    write('    fees: outstanding + paid')


def _seed_lms(school, class_group, student, teacher_user, write):
    maths, _ = CourseSubject.objects.get_or_create(
        school=school,
        name='Maths',
        defaults={'description': 'Mathematics curriculum'},
    )
    track, _ = CourseTrack.objects.get_or_create(
        subject=maths,
        name='Foundation',
        defaults={'description': 'Core number skills', 'sort_order': 0},
    )
    material, _ = CourseMaterial.objects.get_or_create(
        track=track,
        title='Fractions worksheet — showcase',
        defaults={
            'material_type': CourseMaterial.TYPE_WORKSHEET,
            'external_url': 'https://alnoor.example/lms/fractions',
            'sort_order': 0,
        },
    )
    ClassTrackAssignment.objects.get_or_create(
        class_group=class_group,
        track=track,
        defaults={'assigned_by': teacher_user},
    )
    prog, _ = StudentMaterialProgress.objects.get_or_create(
        student=student,
        material=material,
    )
    prog.status = StudentMaterialProgress.STATUS_COMPLETED
    prog.progress_percent = 100
    prog.completed_at = timezone.now()
    prog.save()
    MaterialSubmission.objects.get_or_create(
        student=student,
        material=material,
        defaults={
            'file': ContentFile(b'Amina showcase worksheet', name=f'{student.admission_number}.pdf'),
            'notes': 'Completed all questions.',
            'status': MaterialSubmission.STATUS_APPROVED,
            'teacher_feedback': 'Excellent — full marks.',
            'reviewed_by': teacher_user,
            'reviewed_at': timezone.now(),
        },
    )
    write('    lms: completed worksheet')


def _seed_notifications(school, parent_user, student_user, student_profile, write):
    notify_user(
        user=parent_user,
        school=school,
        notification_type='signoff',
        title=f'{student_profile.full_name} passed Juz 3',
        message='Congratulations! Amina Hassan has passed Juz 3.',
        link_path='/hifz/',
    )
    notify_user(
        user=student_user,
        school=school,
        notification_type='signoff',
        title='Homework approved',
        message='Your maths homework was signed off — well done!',
        link_path='/worksheets/',
    )
    Notification.objects.get_or_create(
        user=parent_user,
        school=school,
        title='Attendance updated',
        defaults={
            'notification_type': 'attendance',
            'message': f'Attendance register updated for {student_profile.full_name}.',
            'link_path': '/attendance/',
        },
    )
    write('    notifications: parent + student')

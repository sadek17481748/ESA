"""
Rich demo content for Al-Noor Academy — homework, exams, Quran, LMS, attendance,
behaviour, messaging, fees, and notifications. Idempotent; safe to re-run.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone

from academics.models import BehaviourRecord, ClassEnrollment, ClassGroup
from attendance.models import AttendanceMark, AttendanceSession
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
from pages.attendance_service import get_or_create_session
from parents.models import ParentProfile, StudentParentLink
from payments.models import FeeItem
from quran.models import QuranAnnotation, QuranSession
from quran.services import mark_session_reviewed, save_page_markup
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile

User = get_user_model()

CONTENT_MARKER_TITLE = 'Al-Noor Spring maths homework'
STUDENT_PASSWORD = 'student1234'
PARENT_PASSWORD = 'parent1234'
TEACHER_PASSWORD = 'teacher1234'


def seed_alnoor_rich_content(school, *, stdout=None):
    """Populate a functioning school demo — call after structural seed."""
    write = stdout.write if stdout else (lambda msg: None)

    if Assignment.objects.filter(school=school, title__contains='Spring maths homework').exists():
        write('  rich content already seeded — refreshing attendance + fees')
        _seed_attendance(school, write)
        _seed_fees(school, write)
        _export_login_reference(school, write)
        return

    teachers = _teacher_map(school)
    classes = list(ClassGroup.objects.filter(school=school).select_related('year_group').order_by('name'))
    subjects = {s.name: s for s in Subject.objects.filter(school=school)}

    write('  seeding LMS tracks and materials…')
    lms_by_class = _seed_lms(school, classes, teachers, write)

    write('  seeding homework and worksheets…')
    _seed_homework(school, classes, subjects, teachers, write)

    write('  seeding exams with sign-offs…')
    _seed_exams(school, classes, subjects, teachers, write)

    write('  seeding Quran / Hifz sessions…')
    _seed_quran(school, classes, teachers, write)

    write('  seeding Hifz juz sign-offs…')
    _seed_hifz_signoffs(school, teachers, write)

    write('  seeding attendance registers…')
    _seed_attendance(school, write)

    write('  seeding behaviour records…')
    _seed_behaviour(school, classes, teachers, write)

    write('  seeding messages and teacher reports…')
    _seed_messaging(school, classes, teachers, write)

    write('  seeding parent fees…')
    _seed_fees(school, write)

    write('  seeding notifications…')
    _seed_notifications(school, write)

    _export_login_reference(school, write)
    write('  Al-Noor rich content complete.')


def _teacher_map(school):
    profiles = list(TeacherProfile.objects.filter(school=school).select_related('user'))
    by_username = {p.user.username: p for p in profiles}
    by_subject = {}
    for p in profiles:
        key = (p.subject or '').lower()
        if key and key not in by_subject:
            by_subject[key] = p
    return {
        'by_username': by_username,
        'by_subject': by_subject,
        'quran': by_username.get('mr_mohammed') or by_subject.get('quran'),
        'maths': by_subject.get('maths'),
        'english': by_subject.get('english') or by_subject.get('quran'),
        'arabic': by_subject.get('arabic'),
        'default': by_username.get('mr_mohammed') or (profiles[0] if profiles else None),
    }


def _class_teacher(class_group, teachers):
    name = class_group.name
    if name.endswith('A'):
        return teachers['quran'] or teachers['default']
    if name.endswith('B'):
        return teachers['maths'] or teachers['default']
    return teachers['default']


def _seed_lms(school, classes, teachers, write):
    lms_by_class = {}
    subject_specs = (
        ('Maths', 'Foundation', ('Place value recap', 'Fractions drill', 'Algebra intro')),
        ('English', 'Core', ('Reading log week 4', 'Persuasive writing task')),
        ('Quran', 'Hifz support', ('Tajweed — noon sakinah', 'Memorisation check — Juz Amma')),
    )
    for subj_name, track_name, materials in subject_specs:
        course_subj, _ = CourseSubject.objects.get_or_create(
            school=school, name=subj_name,
            defaults={'description': f'{subj_name} curriculum at Al-Noor'},
        )
        track, _ = CourseTrack.objects.get_or_create(
            subject=course_subj, name=track_name,
            defaults={'description': f'{subj_name} {track_name}', 'sort_order': 0},
        )
        for i, title in enumerate(materials):
            CourseMaterial.objects.get_or_create(
                track=track, title=title,
                defaults={
                    'material_type': CourseMaterial.TYPE_WORKSHEET,
                    'external_url': f'https://alnoor.example/lms/{subj_name.lower()}/{i}',
                    'sort_order': i,
                },
            )

    maths_track = CourseTrack.objects.filter(
        subject__school=school, subject__name='Maths',
    ).first()
    english_track = CourseTrack.objects.filter(
        subject__school=school, subject__name='English',
    ).first()
    quran_track = CourseTrack.objects.filter(
        subject__school=school, subject__name='Quran',
    ).first()

    for class_group in classes:
        teacher_user = (_class_teacher(class_group, teachers) or teachers['default']).user
        for track in (maths_track, english_track, quran_track):
            if track:
                ClassTrackAssignment.objects.get_or_create(
                    class_group=class_group, track=track,
                    defaults={'assigned_by': teacher_user},
                )

        students = StudentProfile.objects.filter(
            class_enrollments__class_group=class_group, is_active=True,
        ).distinct()
        first_material = CourseMaterial.objects.filter(track=maths_track).order_by('sort_order').first()
        for idx, student in enumerate(students):
            if first_material:
                status = StudentMaterialProgress.STATUS_COMPLETED if idx % 3 == 0 else (
                    StudentMaterialProgress.STATUS_IN_PROGRESS if idx % 3 == 1
                    else StudentMaterialProgress.STATUS_NOT_STARTED
                )
                pct = 100 if status == StudentMaterialProgress.STATUS_COMPLETED else (55 if idx % 3 == 1 else 0)
                prog, _ = StudentMaterialProgress.objects.get_or_create(
                    student=student, material=first_material,
                )
                prog.status = status
                prog.progress_percent = pct
                if status == StudentMaterialProgress.STATUS_COMPLETED:
                    prog.completed_at = timezone.now()
                prog.save()

            if first_material and idx % 4 == 0:
                MaterialSubmission.objects.get_or_create(
                    student=student, material=first_material,
                    defaults={
                        'file': ContentFile(
                            b'Al-Noor worksheet submission',
                            name=f'{student.admission_number}-worksheet.pdf',
                        ),
                        'notes': 'Completed worksheet — please review.',
                        'status': (
                            MaterialSubmission.STATUS_APPROVED
                            if idx % 8 == 0 else MaterialSubmission.STATUS_PENDING
                        ),
                        'teacher_feedback': 'Excellent working shown.' if idx % 8 == 0 else '',
                        'reviewed_by': teacher_user if idx % 8 == 0 else None,
                        'reviewed_at': timezone.now() if idx % 8 == 0 else None,
                    },
                )
        lms_by_class[class_group.name] = maths_track
    return lms_by_class


def _seed_homework(school, classes, subjects, teachers, write):
    today = date.today()
    for class_group in classes:
        maths = subjects.get('Maths')
        english = subjects.get('English')
        teacher = teachers['maths'] or _class_teacher(class_group, teachers)
        if not teacher or not maths:
            continue

        hw, _ = Assignment.objects.get_or_create(
            school=school, class_group=class_group,
            title=f'Spring maths homework — {class_group.name}',
            defaults={
                'subject': maths,
                'teacher': teacher,
                'description': 'Complete exercises 1–8. Show full working.',
                'assignment_type': Assignment.TYPE_HOMEWORK,
                'due_date': today + timedelta(days=7),
            },
        )
        ws, _ = Assignment.objects.get_or_create(
            school=school, class_group=class_group,
            title=f'Fractions worksheet — {class_group.name}',
            defaults={
                'subject': maths,
                'teacher': teacher,
                'description': 'Print and complete the attached worksheet.',
                'assignment_type': Assignment.TYPE_WORKSHEET,
                'due_date': today + timedelta(days=3),
            },
        )
        if english:
            Assignment.objects.get_or_create(
                school=school, class_group=class_group,
                title=f'Reading comprehension — {class_group.name}',
                defaults={
                    'subject': english,
                    'teacher': teachers['english'] or teacher,
                    'description': 'Read the passage and answer all questions.',
                    'assignment_type': Assignment.TYPE_HOMEWORK,
                    'due_date': today + timedelta(days=5),
                },
            )

        for assignment in (hw, ws):
            for enr in ClassEnrollment.objects.filter(class_group=class_group).select_related('student'):
                student = enr.student
                sub, created = Submission.objects.get_or_create(
                    assignment=assignment, student=student,
                    defaults={
                        'body': f'Submission from {student.full_name} for {assignment.title}.',
                        'status': Submission.STATUS_SUBMITTED,
                        'submitted_at': timezone.now() - timedelta(days=1),
                    },
                )
                if not created and sub.status == Submission.STATUS_DRAFT:
                    sub.status = Submission.STATUS_SUBMITTED
                    sub.submitted_at = timezone.now()
                    sub.save()
                if student.admission_number.endswith('001') and sub.status == Submission.STATUS_SUBMITTED:
                    try:
                        sign_off_submission(
                            submission=sub,
                            teacher_profile=assignment.teacher,
                            approve=True,
                            note='Well done — clear working throughout.',
                        )
                    except (PermissionError, ValueError):
                        pass


def _seed_exams(school, classes, subjects, teachers, write):
    today = date.today()
    for class_group in classes:
        maths = subjects.get('Maths')
        teacher = teachers['maths'] or _class_teacher(class_group, teachers)
        if not maths or not teacher:
            continue

        exam, created = Exam.objects.get_or_create(
            school=school, class_group=class_group,
            title=f'Spring maths assessment — {class_group.name}',
            defaults={
                'subject': maths,
                'teacher': teacher,
                'exam_date': today - timedelta(days=14),
                'status': Exam.STATUS_DRAFT,
            },
        )
        if created or not exam.questions.exists():
            ExamQuestion.objects.get_or_create(
                exam=exam, sort_order=0,
                defaults={
                    'question_type': ExamQuestion.TYPE_MCQ,
                    'prompt': 'What is 3/4 + 1/4?',
                    'option_a': '1', 'option_b': '3/8', 'option_c': '2/4', 'option_d': '4/8',
                    'correct_option': 'a', 'max_marks': 2,
                },
            )
            ExamQuestion.objects.get_or_create(
                exam=exam, sort_order=1,
                defaults={
                    'question_type': ExamQuestion.TYPE_WRITTEN,
                    'prompt': 'Explain how to convert 0.75 to a fraction.',
                    'max_marks': 4,
                },
            )

        publish_exam(exam)
        ensure_results_for_exam(exam)
        mcq = exam.questions.filter(question_type=ExamQuestion.TYPE_MCQ).first()
        written = exam.questions.filter(question_type=ExamQuestion.TYPE_WRITTEN).first()

        for enr in ClassEnrollment.objects.filter(class_group=class_group).select_related('student'):
            student = enr.student
            result, _ = ExamResult.objects.get_or_create(exam=exam, student=student)
            answers = {}
            if mcq:
                answers[str(mcq.pk)] = {'selected_option': 'a'}
            if written:
                answers[str(written.pk)] = {
                    'written_answer': f'{student.first_name} explained that 0.75 equals 3/4.',
                }
            save_student_answers(result, answers)
            if written:
                apply_manual_marks(result, {str(written.pk): 3})
            auto_mark_mcq(result)
            if student.admission_number.endswith(('001', '002', '003')):
                try:
                    finalise_result(
                        result=result,
                        teacher_profile=teacher,
                        comment='Strong performance — keep practising problem solving.',
                    )
                except (PermissionError, ValueError):
                    pass


def _seed_quran(school, classes, teachers, write):
    quran_teacher = teachers['quran'] or teachers['default']
    if not quran_teacher:
        return

    for class_group in classes:
        for enr in ClassEnrollment.objects.filter(class_group=class_group).select_related('student'):
            student = enr.student
            session, _ = QuranSession.objects.get_or_create(
                school=school,
                student=student,
                teacher=quran_teacher,
                surah_name='Mushaf',
                defaults={'status': QuranSession.STATUS_SUBMITTED},
            )
            save_page_markup(
                session=session,
                para_number=1,
                page_number=1,
                note='Strong memorisation — focus on madd.',
                highlights=[{'x': 0.15, 'y': 0.25, 'w': 0.4, 'h': 0.04, 'color': '#fff59d'}],
            )
            if student.admission_number.endswith(('001', '002', '003', '004', '005')):
                mark_session_reviewed(
                    session,
                    quran_teacher,
                    notes='Hifz recitation signed off — ready for next surah.',
                )


def _seed_hifz_signoffs(school, teachers, write):
    from hifz.models import HifzJuzSignOff
    from hifz.services import sign_off_hifz_juz

    quran_teacher = teachers['quran'] or teachers['default']
    if not quran_teacher:
        return

    teacher_user = quran_teacher.user
    demo_students = StudentProfile.objects.filter(
        school=school,
        admission_number__in=('7A-001', '7A-002', '8A-001'),
    )
    for student in demo_students:
        for juz in (1, 2):
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


def _seed_attendance(school, write):
    today = date.today()
    statuses = (
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_PRESENT,
        AttendanceMark.STATUS_LATE,
        AttendanceMark.STATUS_ABSENT,
    )
    for class_group in ClassGroup.objects.filter(school=school):
        for day_offset in range(4):
            session_date = today - timedelta(days=day_offset)
            session = get_or_create_session(school, class_group, session_date, None)
            for idx, enr in enumerate(
                ClassEnrollment.objects.filter(class_group=class_group).select_related('student')
            ):
                status = statuses[(idx + day_offset) % len(statuses)]
                AttendanceMark.objects.update_or_create(
                    session=session, student=enr.student,
                    defaults={'status': status, 'note': ''},
                )


def _seed_behaviour(school, classes, teachers, write):
    for class_group in classes:
        teacher_user = (_class_teacher(class_group, teachers) or teachers['default']).user
        enrollments = list(
            ClassEnrollment.objects.filter(class_group=class_group).select_related('student')
        )
        if not enrollments:
            continue
        commend_student = enrollments[0].student
        BehaviourRecord.objects.get_or_create(
            school=school, student=commend_student, title=f'Star pupil — {class_group.name}',
            defaults={
                'teacher': teacher_user,
                'record_type': BehaviourRecord.TYPE_COMMENDATION,
                'notes': 'Excellent manners and participation in class.',
            },
        )
        if len(enrollments) > 1:
            BehaviourRecord.objects.get_or_create(
                school=school, student=enrollments[1].student,
                title=f'Late to lesson — {class_group.name}',
                defaults={
                    'teacher': teacher_user,
                    'record_type': BehaviourRecord.TYPE_INCIDENT,
                    'notes': 'Arrived 10 minutes late — reminder given.',
                },
            )


def _seed_messaging(school, classes, teachers, write):
    super_user = User.objects.filter(username='super', role='super_admin').first()
    school_admin = User.objects.filter(username='schooladmin', school=school).first()
    teacher_user = User.objects.filter(username='mr_mohammed', school=school).first()

    for class_group in classes[:3]:
        student = StudentProfile.objects.filter(
            class_enrollments__class_group=class_group,
            admission_number__endswith='001',
        ).first()
        if not student:
            continue
        link = StudentParentLink.objects.filter(student=student).select_related('parent__user').first()
        if not link:
            continue
        parent_user = link.parent.user

        conv, created = SchoolConversation.objects.get_or_create(
            school=school,
            subject=f'Progress update — {student.full_name}',
            created_by=teacher_user or school_admin,
            recipient_type=SchoolConversation.RECIPIENT_PARENT,
            recipient_user=parent_user,
            defaults={'created_by': teacher_user or school_admin},
        )
        if created or conv.messages.count() < 2:
            if teacher_user:
                SchoolMessage.objects.get_or_create(
                    conversation=conv, sender=teacher_user,
                    defaults={'body': f'{student.first_name} is making excellent progress this term.'},
                )
            SchoolMessage.objects.get_or_create(
                conversation=conv, sender=parent_user,
                defaults={'body': 'JazakAllah khayr — we appreciate the update.'},
            )

        TeacherReport.objects.get_or_create(
            school=school, student=student,
            subject_line=f'Spring report — {student.full_name}',
            defaults={
                'teacher': teacher_user or school_admin,
                'parent': parent_user,
                'period_covered': 'Spring term 2026',
                'strengths': 'Attentive in lessons, homework submitted on time.',
                'areas_for_improvement': 'Continue daily Quran revision.',
                'action_required': 'Sign the reading log each week.',
                'additional_notes': 'Parents evening: Thursday 4pm.',
            },
        )

    parent_7a = User.objects.filter(username='parent_7a_01', school=school).first()
    if parent_7a and super_user:
        case, _ = SupportCase.objects.get_or_create(
            case_number='ESA-00001',
            defaults={
                'opened_by': parent_7a,
                'subject': 'Cannot see homework on mobile',
                'status': SupportCase.STATUS_OPEN,
            },
        )
        SupportMessage.objects.get_or_create(
            case=case, sender=parent_7a,
            defaults={'body': 'Homework page empty on mobile — works on laptop.'},
        )
        SupportMessage.objects.get_or_create(
            case=case, sender=super_user,
            defaults={
                'body': 'Thank you — we are rolling out a mobile fix this week.',
                'is_staff_reply': True,
            },
        )


def _seed_fees(school, write):
    today = date.today()
    for link in StudentParentLink.objects.filter(
        parent__user__school=school,
    ).select_related('parent__user', 'student'):
        parent = link.parent.user
        child = link.student
        FeeItem.objects.get_or_create(
            school=school, parent=parent,
            title=f'Term 3 tuition — {child.admission_number}',
            defaults={
                'child_name': child.full_name,
                'description': 'Spring term tuition fees',
                'amount_pence': 25000,
                'due_date': today + timedelta(days=14),
                'status': FeeItem.STATUS_OUTSTANDING,
            },
        )
        if child.admission_number.endswith('002'):
            FeeItem.objects.get_or_create(
                school=school, parent=parent,
                title=f'School trip — {child.admission_number}',
                defaults={
                    'child_name': child.full_name,
                    'amount_pence': 3500,
                    'due_date': today - timedelta(days=3),
                    'status': FeeItem.STATUS_OVERDUE,
                },
            )


def _seed_notifications(school, write):
    for student in StudentProfile.objects.filter(school=school, is_active=True)[:50]:
        if student.user_id:
            Notification.objects.get_or_create(
                user=student.user, school=school,
                title='Welcome to Al-Noor Academy',
                defaults={
                    'notification_type': 'general',
                    'message': 'Your timetable, homework, and Quran sessions are ready.',
                    'link_path': '/dashboard/',
                },
            )
    for parent in ParentProfile.objects.filter(school=school)[:50]:
        Notification.objects.get_or_create(
            user=parent.user, school=school,
            title='Al-Noor parent portal ready',
            defaults={
                'notification_type': 'general',
                'message': 'View attendance, fees, and teacher reports for your children.',
                'link_path': '/dashboard/',
            },
        )


def _export_login_reference(school, write):
    """Write full login CSV and print staff summary."""
    import csv
    from pathlib import Path

    docs_dir = Path(__file__).resolve().parent.parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    csv_path = docs_dir / 'alnoor-academy-logins.csv'

    teachers = User.objects.filter(school=school, role='teacher').order_by('username')
    rows = []

    for t in teachers:
        rows.append({
            'role': 'teacher',
            'class': '',
            'name': t.get_full_name() or t.username,
            'username': t.username,
            'password': TEACHER_PASSWORD if t.username != 'msadekhussain2001@gmail.com' else 'Teacher2026!',
            'linked_parent': '',
            'admission': '',
        })

    for class_group in ClassGroup.objects.filter(school=school).order_by('name'):
        code = class_group.name.lower().replace(' ', '')
        for i in range(1, 31):
            student_u = f'student_{code}_{i:02d}'
            parent_u = f'parent_{code}_{i:02d}'
            student = StudentProfile.objects.filter(
                user__username=student_u, school=school,
            ).select_related('user').first()
            rows.append({
                'role': 'student',
                'class': class_group.name,
                'name': student.full_name if student else '',
                'username': student_u,
                'password': STUDENT_PASSWORD,
                'linked_parent': parent_u,
                'admission': student.admission_number if student else '',
            })
            rows.append({
                'role': 'parent',
                'class': class_group.name,
                'name': student.full_name if student else '',
                'username': parent_u,
                'password': PARENT_PASSWORD,
                'linked_parent': '',
                'admission': student.admission_number if student else '',
            })

    with csv_path.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=['role', 'class', 'name', 'username', 'password', 'linked_parent', 'admission'],
        )
        writer.writeheader()
        writer.writerows(rows)

    write(f'  login reference exported → {csv_path} ({len(rows)} rows)')

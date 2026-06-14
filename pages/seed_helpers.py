"""Shared helpers for idempotent demo seeding — preserve passwords on deploy."""
from django.contrib.auth import get_user_model

User = get_user_model()

# Only these accounts get passwords reset on every Heroku boot.
PUBLIC_DEMO_USERNAMES = frozenset({'schooladmin', 'super', 'parent_demo'})

PERSONAL_PARENT_EMAIL = 'msadekhussain@outlook.com'
PERSONAL_TEACHER_EMAIL = 'msadekhussain2001@gmail.com'
PERSONAL_PARENT_PASSWORD = 'Parent2026!'
PERSONAL_TEACHER_PASSWORD = 'Teacher2026!'


def should_reset_password(username, *, created):
    if username in PUBLIC_DEMO_USERNAMES:
        return True
    return created


def upsert_user(
    username,
    *,
    email,
    role,
    password,
    school=None,
    first_name='',
    last_name='',
    email_verified=True,
    force_reset_password=None,
):
    """
    Create or update a user without wiping passwords on every deploy.
    force_reset_password: True/False overrides the default policy.
    """
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email},
    )
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.role = role
    user.school = school
    user.is_active = True
    user.email_verified = email_verified

    if force_reset_password is None:
        reset = should_reset_password(username, created=created)
    else:
        reset = force_reset_password

    if reset:
        user.set_password(password)

    user.save()
    return user, created


def sync_personal_accounts(school, *, stdout=None):
    """Fast sync of permanent outlook/gmail accounts — safe to run on every deploy."""
    from parents.models import ParentProfile, StudentParentLink
    from students.models import StudentProfile
    from teachers.models import TeacherProfile
    from timetable.models import Timetable, TimetableSlot

    write = stdout.write if stdout else (lambda msg: None)

    linked_student = StudentProfile.objects.filter(
        school=school,
        admission_number='7A-001',
    ).select_related('user').first()
    if not linked_student:
        linked_student = StudentProfile.objects.filter(school=school).first()

    teacher_user, t_created = upsert_user(
        PERSONAL_TEACHER_EMAIL,
        email=PERSONAL_TEACHER_EMAIL,
        role='teacher',
        password=PERSONAL_TEACHER_PASSWORD,
        school=school,
        first_name='Mohammed',
        last_name='Hussain',
    )
    teacher_profile, _ = TeacherProfile.objects.get_or_create(
        user=teacher_user,
        defaults={'school': school, 'subject': 'Maths'},
    )
    teacher_profile.school = school
    teacher_profile.subject = 'Maths'
    teacher_profile.save()

    parent_user, p_created = upsert_user(
        PERSONAL_PARENT_EMAIL,
        email=PERSONAL_PARENT_EMAIL,
        role='parent',
        password=PERSONAL_PARENT_PASSWORD,
        school=school,
        first_name='Mohammed',
        last_name='Hussain',
    )
    StudentProfile.objects.filter(user=parent_user).delete()

    parent_profile, _ = ParentProfile.objects.get_or_create(
        user=parent_user,
        defaults={'school': school},
    )

    if linked_student:
        StudentParentLink.objects.get_or_create(
            parent=parent_profile,
            student=linked_student,
            defaults={'relationship': 'father'},
        )
        timetable = (
            Timetable.objects.filter(
                school=school,
                class_group__name='7A',
                is_active=True,
            )
            .order_by('-updated_at')
            .first()
        )
        if timetable:
            TimetableSlot.objects.filter(
                timetable=timetable,
                subject__name='Maths',
            ).update(teacher=teacher_profile)

    if t_created or p_created:
        write(f'  personal accounts synced (new: teacher={t_created}, parent={p_created})')
    return teacher_profile, linked_student


def sync_mr_mohammed_attendance_demo(school, *, stdout=None):
    """
    Ensure mr_mohammed has Quran slots on the 7A timetable for attendance screenshots.
    Teachers are not homeroom-fixed — only timetable slots control their schedule.
    """
    from academics.models import ClassGroup
    from teachers.models import TeacherProfile
    from timetable.models import Timetable, TimetableSlot

    write = stdout.write if stdout else (lambda msg: None)

    teacher_profile = TeacherProfile.objects.filter(
        user__username='mr_mohammed',
        school=school,
    ).first()
    class_group = ClassGroup.objects.filter(school=school, name='7A').first()
    if not teacher_profile or not class_group:
        return False

    timetable = (
        Timetable.objects.filter(
            school=school,
            class_group=class_group,
            is_active=True,
        )
        .order_by('-updated_at')
        .first()
    )
    if timetable:
        TimetableSlot.objects.filter(
            timetable=timetable,
            subject__name='Quran',
        ).update(teacher=teacher_profile)

    write('  mr_mohammed → 7A Quran timetable slots (attendance demo)')
    return True

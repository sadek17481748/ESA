"""Hifz sign-off — record pass and notify linked parent."""
from parents.models import StudentParentLink

from messaging.models import SchoolConversation, SchoolMessage
from notifications.services import notify_user

from .models import HifzJuzSignOff


def sign_offs_for_teacher(teacher_user, limit=50):
    return HifzJuzSignOff.objects.filter(signed_off_by=teacher_user).select_related('student')[:limit]


def sign_offs_for_parent(parent_user, limit=50):
    parent_profile = getattr(parent_user, 'parent_profile', None)
    if not parent_profile:
        return []

    student_ids = StudentParentLink.objects.filter(parent=parent_profile).values_list('student_id', flat=True)
    return HifzJuzSignOff.objects.filter(student_id__in=student_ids).select_related(
        'student', 'signed_off_by',
    )[:limit]


def sign_offs_for_student(student_profile, limit=30):
    if not student_profile:
        return []
    return HifzJuzSignOff.objects.filter(student=student_profile).select_related('signed_off_by')[:limit]


def sign_offs_for_school_admin(school, limit=100):
    return HifzJuzSignOff.objects.filter(school=school).select_related('student', 'signed_off_by')[:limit]


def sign_off_hifz_juz(*, student, juz_number, teacher_user):
    school = student.school
    if teacher_user.school_id != school.pk:
        raise PermissionError('You can only sign off students at your school.')

    if HifzJuzSignOff.objects.filter(student=student, juz_number=juz_number).exists():
        raise ValueError(f'Juz {juz_number} is already signed off for {student.full_name}.')

    sign_off = HifzJuzSignOff.objects.create(
        school=school,
        student=student,
        juz_number=juz_number,
        signed_off_by=teacher_user,
    )

    parent_link = StudentParentLink.objects.filter(student=student).select_related('parent__user').first()
    if parent_link:
        parent_user = parent_link.parent.user
        subject = f'Hifz — Juz {juz_number} passed'
        body = (
            f'Congratulations! {student.full_name} has passed Juz {juz_number}. '
            f'This milestone has been signed off by their teacher.'
        )

        conv = SchoolConversation.objects.create(
            school=school,
            subject=subject,
            created_by=teacher_user,
            recipient_type=SchoolConversation.RECIPIENT_PARENT,
            recipient_user=parent_user,
        )
        SchoolMessage.objects.create(
            conversation=conv,
            sender=teacher_user,
            body=body,
        )
        notify_user(
            user=parent_user,
            school=school,
            notification_type='signoff',
            title=f'{student.full_name} passed Juz {juz_number}',
            message=body,
            link_path=f'/messages/school/{conv.pk}/',
        )

    return sign_off

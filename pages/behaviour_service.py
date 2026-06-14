"""Behaviour logging for teachers and read-only parent view."""
from academics.models import BehaviourRecord
from students.models import StudentProfile


def students_for_teacher(school, teacher_user):
    """Teachers may log behaviour or work with any student in their school."""
    return StudentProfile.objects.filter(school=school, is_active=True).order_by('last_name', 'first_name')


def behaviour_for_parent(parent_user, limit=30):
    from parents.models import StudentParentLink

    parent_profile = getattr(parent_user, 'parent_profile', None)
    if not parent_profile:
        return []

    student_ids = StudentParentLink.objects.filter(parent=parent_profile).values_list('student_id', flat=True)
    return BehaviourRecord.objects.filter(student_id__in=student_ids).select_related(
        'student', 'teacher',
    )[:limit]


def behaviour_for_teacher(teacher_user, limit=50):
    return BehaviourRecord.objects.filter(teacher=teacher_user).select_related('student')[:limit]


def behaviour_for_school_admin(school, limit=100):
    return BehaviourRecord.objects.filter(school=school).select_related('student', 'teacher')[:limit]

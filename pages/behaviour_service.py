"""Behaviour logging for teachers and read-only parent view."""
from academics.models import BehaviourRecord, ClassEnrollment
from students.models import StudentProfile


def students_for_teacher(school, teacher_user):
    from teachers.models import TeacherProfile
    from academics.models import ClassGroup

    profile = TeacherProfile.objects.filter(user=teacher_user).first()
    if not profile:
        return StudentProfile.objects.filter(school=school, is_active=True).order_by('last_name')

    class_ids = ClassGroup.objects.filter(school=school, teacher=profile).values_list('pk', flat=True)
    student_ids = ClassEnrollment.objects.filter(class_group_id__in=class_ids).values_list('student_id', flat=True)
    return StudentProfile.objects.filter(pk__in=student_ids, is_active=True).distinct().order_by('last_name')


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

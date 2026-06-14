"""pages/enrollment_service.py — student class enrollment and class content."""
from academics.models import ClassEnrollment, ClassGroup
from students.models import StudentProfile

from .timetable_service import PERIODS, build_timetable_grid, list_live_timetables


def enroll_student(student, class_group):
    """Assign a student to a class (one active enrollment per student)."""
    ClassEnrollment.objects.filter(student=student).delete()
    enrollment = ClassEnrollment.objects.create(
        class_group=class_group,
        student=student,
    )
    if class_group.year_group_id:
        student.year_group = class_group.year_group.name
    else:
        student.year_group = class_group.name
    student.school = class_group.school
    student.save(update_fields=['year_group', 'school'])
    return enrollment


def student_profile_for_user(user):
    if user.role != 'student':
        return None
    return StudentProfile.objects.filter(user=user).first()


def student_class_group(student):
    if not student:
        return None
    enrollment = (
        ClassEnrollment.objects.filter(student=student)
        .select_related('class_group', 'class_group__teacher', 'class_group__teacher__user')
        .first()
    )
    return enrollment.class_group if enrollment else None


def student_needs_class(user):
    profile = student_profile_for_user(user)
    return profile is not None and student_class_group(profile) is None


def classes_for_school(school):
    return ClassGroup.objects.filter(school=school).order_by('name')


def student_portal_context(student):
    """Timetable grid and subjects for a student's class."""
    class_group = student_class_group(student)
    if not class_group:
        return {
            'class_group': None,
            'timetable': None,
            'grid': {},
            'timetable_rows': [],
            'periods': [],
            'weekday_labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'subjects': [],
        }

    timetable_qs = list_live_timetables(class_group.school).filter(class_group=class_group)
    timetable = timetable_qs.order_by('-slot_count', '-updated_at').first()
    if not timetable:
        timetable = (
            list_live_timetables(class_group.school)
            .filter(class_group__isnull=True)
            .first()
        )

    grid = build_timetable_grid(timetable) if timetable else {}
    grid_json = {f'{w}-{t}': v for (w, t), v in grid.items()}
    periods = [
        {'start': s.strftime('%H:%M'), 'end': e.strftime('%H:%M'), 'label': s.strftime('%H:%M')}
        for s, e in PERIODS
    ]
    weekdays = list(range(7))
    timetable_rows = []
    for period in periods:
        timetable_rows.append({
            'label': period['label'],
            'cells': [grid_json.get(f'{wd}-{period["start"]}') for wd in weekdays],
        })
    subject_names = sorted({v['subject_name'] for v in grid_json.values()})

    return {
        'class_group': class_group,
        'timetable': timetable,
        'grid': grid_json,
        'timetable_rows': timetable_rows,
        'periods': periods,
        'weekday_labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'weekdays': weekdays,
        'subjects': subject_names,
    }

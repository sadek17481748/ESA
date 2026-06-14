"""pages/attendance_service.py — portal attendance registers and overview."""
from datetime import date

from django.db.models import Count, Q

from academics.models import ClassEnrollment, ClassGroup
from attendance.models import AttendanceMark, AttendanceSession
from students.models import StudentProfile


def session_date_or_today(value=None):
    if value:
        return value
    return date.today()


def students_in_class(class_group):
    return StudentProfile.objects.filter(
        class_enrollments__class_group=class_group,
        is_active=True,
    ).order_by('last_name', 'first_name')


def get_session(class_group, session_date):
    return AttendanceSession.objects.filter(
        class_group=class_group,
        session_date=session_date,
    ).prefetch_related('marks').first()


def get_or_create_session(school, class_group, session_date, taken_by):
    session, _ = AttendanceSession.objects.get_or_create(
        school=school,
        class_group=class_group,
        session_date=session_date,
        defaults={'taken_by': taken_by},
    )
    if not session.taken_by_id and taken_by:
        session.taken_by = taken_by
        session.save(update_fields=['taken_by'])
    return session


def marks_for_session(session):
    if not session:
        return {}
    return {m.student_id: m for m in session.marks.all()}


def build_class_register(class_group, session_date):
    """Students and current marks for one class on a date."""
    session = get_session(class_group, session_date)
    marks = marks_for_session(session)
    rows = []
    for student in students_in_class(class_group):
        mark = marks.get(student.pk)
        rows.append({
            'student': student,
            'status': mark.status if mark else AttendanceMark.STATUS_PRESENT,
            'note': mark.note if mark else '',
            'has_mark': mark is not None,
        })
    return {
        'class_group': class_group,
        'session': session,
        'session_date': session_date,
        'rows': rows,
        'student_count': len(rows),
    }


def save_class_register(school, class_group, session_date, taken_by, marks_payload):
    """
    marks_payload: {student_id: {'status': 'present'|'late'|'absent', 'note': ''}, ...}
    """
    enrolled_ids = set(
        ClassEnrollment.objects.filter(class_group=class_group).values_list('student_id', flat=True)
    )
    session = get_or_create_session(school, class_group, session_date, taken_by)
    AttendanceMark.objects.filter(session=session).delete()
    created = 0
    for student_id, data in marks_payload.items():
        sid = int(student_id)
        if sid not in enrolled_ids:
            continue
        status = data.get('status', AttendanceMark.STATUS_PRESENT)
        if status not in dict(AttendanceMark.STATUS_CHOICES):
            status = AttendanceMark.STATUS_PRESENT
        AttendanceMark.objects.create(
            session=session,
            student_id=sid,
            status=status,
            note=(data.get('note') or '')[:200],
        )
        created += 1
    return session, created


def build_school_attendance_overview(school, session_date):
    """All classes with enrolled students and today's attendance summary."""
    classes = ClassGroup.objects.filter(school=school).annotate(
        enrolled_count=Count('enrollments'),
    ).select_related('teacher', 'teacher__user').order_by('name')

    overview = []
    totals = {'students': 0, 'present': 0, 'late': 0, 'absent': 0, 'unmarked': 0}

    for class_group in classes:
        register = build_class_register(class_group, session_date)
        present = late = absent = unmarked = 0
        student_rows = []
        for row in register['rows']:
            totals['students'] += 1
            if not register['session']:
                unmarked += 1
                totals['unmarked'] += 1
            elif row['status'] == AttendanceMark.STATUS_PRESENT:
                present += 1
                totals['present'] += 1
            elif row['status'] == AttendanceMark.STATUS_LATE:
                late += 1
                totals['late'] += 1
            else:
                absent += 1
                totals['absent'] += 1
            student_rows.append(row)

        overview.append({
            'class_group': class_group,
            'enrolled_count': class_group.enrolled_count,
            'register': register,
            'rows': student_rows,
            'present': present,
            'late': late,
            'absent': absent,
            'unmarked': unmarked,
            'has_session': register['session'] is not None,
        })

    return overview, totals, session_date


def teacher_classes(school, teacher_profile):
    """Homeroom classes plus any class this teacher is assigned on the timetable."""
    if not teacher_profile:
        return ClassGroup.objects.none()
    from timetable.models import TimetableSlot

    slot_class_ids = TimetableSlot.objects.filter(
        teacher=teacher_profile,
        school=school,
        timetable__is_active=True,
    ).values_list('class_group_id', flat=True)
    return ClassGroup.objects.filter(
        Q(school=school) & (Q(teacher=teacher_profile) | Q(pk__in=slot_class_ids)),
    ).select_related('teacher', 'teacher__user').order_by('name').distinct()


def teacher_can_access_class(teacher_profile, class_group):
    """Homeroom teacher or assigned on an active timetable slot for this class."""
    if not teacher_profile or not class_group:
        return False
    if class_group.teacher_id == teacher_profile.pk:
        return True
    from timetable.models import TimetableSlot

    return TimetableSlot.objects.filter(
        teacher=teacher_profile,
        class_group=class_group,
        timetable__is_active=True,
    ).exists()


def class_labels_for_teacher(school, teacher_profile):
    """Map class id → display label including subjects taught (e.g. 2C — Maths, Science)."""
    from timetable.models import TimetableSlot

    labels = {}
    for class_group in teacher_classes(school, teacher_profile):
        labels[class_group.pk] = class_group.name

    slot_rows = (
        TimetableSlot.objects.filter(
            teacher=teacher_profile,
            school=school,
            timetable__is_active=True,
        )
        .select_related('class_group', 'subject')
        .order_by('class_group__name', 'subject__name')
    )
    subjects_by_class = {}
    for slot in slot_rows:
        subjects_by_class.setdefault(slot.class_group_id, set()).add(slot.subject.name)

    for class_id, subjects in subjects_by_class.items():
        class_name = next(
            (s.class_group.name for s in slot_rows if s.class_group_id == class_id),
            labels.get(class_id, ''),
        )
        if subjects:
            labels[class_id] = f'{class_name} — {", ".join(sorted(subjects))}'

    return labels


def student_attendance_history(student, limit=30):
    return (
        AttendanceMark.objects.filter(student=student)
        .select_related('session', 'session__class_group')
        .order_by('-session__session_date')[:limit]
    )


def parent_children_attendance(parent_user, session_date=None):
    from parents.models import StudentParentLink

    session_date = session_date_or_today(session_date)
    parent_profile = getattr(parent_user, 'parent_profile', None)
    if not parent_profile:
        return []

    children = []
    for link in StudentParentLink.objects.filter(parent=parent_profile).select_related('student'):
        student = link.student
        class_group = student_class_group_for(student)
        history = student_attendance_history(student, limit=14)
        today_mark = None
        if class_group:
            session = get_session(class_group, session_date)
            if session:
                today_mark = marks_for_session(session).get(student.pk)
        children.append({
            'student': student,
            'class_group': class_group,
            'today_mark': today_mark,
            'history': history,
        })
    return children


def student_class_group_for(student):
    enrollment = ClassEnrollment.objects.filter(student=student).select_related('class_group').first()
    return enrollment.class_group if enrollment else None

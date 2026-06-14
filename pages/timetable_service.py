"""
pages/timetable_service.py
Timetable subjects, periods, named timetables, and save helpers for the portal builder.
"""
from datetime import time

from django.utils import timezone

from academics.models import ClassGroup
from subjects.models import Subject
from teachers.models import TeacherProfile
from timetable.models import Timetable, TimetableSlot

STANDARD_SUBJECTS = (
    ('English', Subject.TRACK_GENERAL, 'ENG'),
    ('Maths', Subject.TRACK_GENERAL, 'MAT'),
    ('Science', Subject.TRACK_GENERAL, 'SCI'),
    ('Arabic', Subject.TRACK_GENERAL, 'ARB'),
    ('Quran', Subject.TRACK_HIFZ, 'QUR'),
    ('Alimiyah', Subject.TRACK_ALIMIYAH, 'ALI'),
)

PERIODS = (
    (time(8, 30), time(9, 15)),
    (time(9, 15), time(10, 0)),
    (time(10, 15), time(11, 0)),
    (time(11, 0), time(11, 45)),
    (time(12, 30), time(13, 15)),
    (time(13, 15), time(14, 0)),
    (time(14, 15), time(15, 0)),
)

WEEKDAYS = list(range(7))


def ensure_school_subjects(school):
    """Create standard subjects if missing."""
    for name, track, code in STANDARD_SUBJECTS:
        Subject.objects.get_or_create(
            school=school,
            name=name,
            defaults={'track': track, 'code': code},
        )


def list_school_subjects(school):
    ensure_school_subjects(school)
    return Subject.objects.filter(school=school, is_active=True).order_by('name')


def list_school_teachers(school):
    return TeacherProfile.objects.filter(school=school).select_related('user').order_by(
        'user__last_name', 'user__first_name',
    )


def teacher_display(profile):
    if not profile:
        return ''
    return profile.user.get_full_name() or profile.user.username


def teachers_for_json(school):
    return [
        {
            'id': t.pk,
            'name': teacher_display(t),
            'username': t.user.username,
        }
        for t in list_school_teachers(school)
    ]


def create_subject(school, *, name, track=Subject.TRACK_GENERAL, code=''):
    name = name.strip()
    if not name:
        raise ValueError('Subject name is required.')
    subject, created = Subject.objects.get_or_create(
        school=school,
        name=name,
        defaults={'track': track, 'code': code.strip()},
    )
    if not created and not subject.is_active:
        subject.is_active = True
        subject.save(update_fields=['is_active'])
    return subject


def list_live_timetables(school):
    """All active timetables for the school hub — with lesson counts."""
    from django.db.models import Count

    return Timetable.objects.filter(school=school, is_active=True).annotate(
        slot_count=Count('slots'),
    ).select_related(
        'class_group', 'class_group__teacher', 'class_group__teacher__user',
    ).order_by('-updated_at', 'name')


def list_timetables(school, class_group=None):
    qs = Timetable.objects.filter(school=school, is_active=True).select_related(
        'class_group', 'class_group__teacher', 'class_group__teacher__user',
    )
    if class_group:
        qs = qs.filter(class_group=class_group)
    return qs.order_by('-updated_at', 'name')


def get_or_create_default_timetable(school, class_group):
    timetable = Timetable.objects.filter(
        school=school, class_group=class_group, is_active=True,
    ).order_by('-updated_at').first()
    if timetable:
        return timetable
    base_name = f'{class_group.name} timetable'
    name = base_name
    suffix = 2
    while Timetable.objects.filter(school=school, name=name).exists():
        name = f'{base_name} ({suffix})'
        suffix += 1
    return Timetable.objects.create(
        school=school,
        name=name,
        class_group=class_group,
    )


def create_timetable(school, *, name, class_group=None, notes=''):
    name = name.strip()
    if not name:
        raise ValueError('Timetable name is required.')
    return Timetable.objects.create(
        school=school,
        name=name,
        class_group=class_group,
        notes=notes.strip(),
    )


def rename_timetable(timetable, *, name, notes=None):
    timetable.name = name.strip()
    if notes is not None:
        timetable.notes = notes.strip()
    timetable.save()
    return timetable


def user_can_edit_timetable(user, timetable, teacher_profile=None):
    if user.role == 'school_admin':
        return True
    if user.role != 'teacher' or not teacher_profile:
        return False
    if timetable.class_group_id is None:
        return True
    return timetable.class_group.teacher_id == teacher_profile.pk


def build_timetable_grid(timetable):
    """Existing slots keyed by (weekday, start_time string)."""
    slots = {}
    for slot in TimetableSlot.objects.filter(timetable=timetable).select_related(
        'subject', 'teacher', 'teacher__user',
    ):
        key = (slot.weekday, slot.start_time.strftime('%H:%M'))
        slots[key] = {
            'id': slot.pk,
            'subject_id': slot.subject_id,
            'subject_name': slot.subject.name,
            'teacher_id': slot.teacher_id,
            'teacher_name': teacher_display(slot.teacher),
            'room': slot.room,
        }
    return slots


def teacher_assigned_slots(teacher_profile, school):
    if not teacher_profile or not school:
        return TimetableSlot.objects.none()
    return TimetableSlot.objects.filter(
        teacher=teacher_profile,
        school=school,
        timetable__is_active=True,
    ).select_related('class_group', 'subject', 'timetable').order_by('weekday', 'start_time')


def _period_rows():
    return [
        {'start': s.strftime('%H:%M'), 'end': e.strftime('%H:%M'), 'label': s.strftime('%H:%M')}
        for s, e in PERIODS
    ]


def teacher_portal_context(teacher_profile, school):
    """Personal schedule from timetable slots assigned to this teacher."""
    weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    periods = _period_rows()
    empty = {
        'has_schedule': False,
        'timetable_rows': [],
        'periods': periods,
        'weekday_labels': weekday_labels,
        'subjects': [],
        'today_slots': [],
        'slot_count': 0,
    }
    if not teacher_profile:
        return empty

    from datetime import date

    slots = list(teacher_assigned_slots(teacher_profile, school))
    if not slots:
        return empty

    grid = {}
    for slot in slots:
        key = (slot.weekday, slot.start_time.strftime('%H:%M'))
        grid[key] = {
            'id': slot.pk,
            'subject_name': slot.subject.name,
            'class_group_id': slot.class_group_id,
            'class_name': slot.class_group.name,
        }

    grid_json = {f'{w}-{t}': v for (w, t), v in grid.items()}
    weekdays = list(range(7))
    timetable_rows = []
    for period in periods:
        timetable_rows.append({
            'label': period['label'],
            'cells': [grid_json.get(f'{wd}-{period["start"]}') for wd in weekdays],
        })

    today_weekday = date.today().weekday()
    today_slots = [
        {
            'id': slot.pk,
            'subject_name': slot.subject.name,
            'class_name': slot.class_group.name,
            'class_group_id': slot.class_group_id,
            'time_label': slot.start_time.strftime('%H:%M'),
        }
        for slot in slots
        if slot.weekday == today_weekday
    ]

    return {
        'has_schedule': True,
        'timetable_rows': timetable_rows,
        'periods': periods,
        'weekday_labels': weekday_labels,
        'subjects': sorted({slot.subject.name for slot in slots}),
        'today_slots': today_slots,
        'slot_count': len(slots),
    }


def save_timetable(timetable, class_group, slot_payload):
    """
    Replace all slots for a timetable from portal JSON:
    [{weekday, start_time, end_time, subject_id, teacher_id?, room?}, ...]
    """
    TimetableSlot.objects.filter(timetable=timetable).delete()
    created = []
    for row in slot_payload:
        subject_id = row.get('subject_id')
        if not subject_id:
            continue
        start_parts = [int(x) for x in row['start_time'].split(':')]
        end_parts = [int(x) for x in row['end_time'].split(':')]
        teacher_id = row.get('teacher_id') or None
        slot = TimetableSlot.objects.create(
            school=timetable.school,
            timetable=timetable,
            class_group=class_group,
            subject_id=subject_id,
            teacher_id=teacher_id,
            weekday=int(row['weekday']),
            start_time=time(start_parts[0], start_parts[1]),
            end_time=time(end_parts[0], end_parts[1]),
            room=row.get('room', ''),
        )
        created.append(slot)
    timetable.updated_at = timezone.now()
    timetable.save(update_fields=['updated_at'])
    return created

"""
pages/timetable_service.py
Timetable subjects, periods, and save helpers for the portal builder.
"""
from datetime import time

from subjects.models import Subject
from timetable.models import TimetableSlot

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
    """Create English, Maths, Science, Arabic, Quran, Alimiyah if missing."""
    subjects = []
    for name, track, code in STANDARD_SUBJECTS:
        subject, _ = Subject.objects.get_or_create(
            school=school,
            name=name,
            defaults={'track': track, 'code': code},
        )
        subjects.append(subject)
    return subjects


def build_timetable_grid(class_group):
    """Existing slots keyed by (weekday, start_time string)."""
    slots = {}
    for slot in TimetableSlot.objects.filter(class_group=class_group).select_related(
        'subject', 'teacher', 'teacher__user',
    ):
        key = (slot.weekday, slot.start_time.strftime('%H:%M'))
        teacher_name = ''
        if slot.teacher_id and slot.teacher.user:
            teacher_name = slot.teacher.user.get_full_name() or slot.teacher.user.username
        slots[key] = {
            'id': slot.pk,
            'subject_id': slot.subject_id,
            'subject_name': slot.subject.name,
            'teacher_name': teacher_name,
        }
    return slots


def save_timetable(class_group, teacher_profile, slot_payload):
    """
    Replace all slots for a class from portal JSON:
    [{weekday, start_time, end_time, subject_id}, ...]
    """
    TimetableSlot.objects.filter(class_group=class_group).delete()
    created = []
    for row in slot_payload:
        subject_id = row.get('subject_id')
        if not subject_id:
            continue
        start_parts = [int(x) for x in row['start_time'].split(':')]
        end_parts = [int(x) for x in row['end_time'].split(':')]
        slot = TimetableSlot.objects.create(
            school=class_group.school,
            class_group=class_group,
            subject_id=subject_id,
            teacher=teacher_profile,
            weekday=int(row['weekday']),
            start_time=time(start_parts[0], start_parts[1]),
            end_time=time(end_parts[0], end_parts[1]),
            room=row.get('room', ''),
        )
        created.append(slot)
    return created

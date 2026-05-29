"""
attendance/models.py
Daily register per class — linked to timetable slot when available.
"""
from django.conf import settings
from django.db import models

from academics.models import ClassGroup
from schools.models import School
from students.models import StudentProfile
from timetable.models import TimetableSlot


class AttendanceSession(models.Model):
    """One register taken for a class on a date."""

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='attendance_sessions')
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='attendance_sessions')
    timetable_slot = models.ForeignKey(
        TimetableSlot, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='attendance_sessions',
    )
    session_date = models.DateField()
    taken_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='registers_taken',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('class_group', 'session_date')]
        ordering = ['-session_date']

    def __str__(self):
        return f'{self.class_group.name} — {self.session_date}'


class AttendanceMark(models.Model):
    STATUS_PRESENT = 'present'
    STATUS_LATE = 'late'
    STATUS_ABSENT = 'absent'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_LATE, 'Late'),
        (STATUS_ABSENT, 'Absent'),
    ]

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='marks')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='attendance_marks')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PRESENT)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = [('session', 'student')]

    def __str__(self):
        return f'{self.student} — {self.status}'

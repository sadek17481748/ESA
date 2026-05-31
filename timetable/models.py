"""
timetable/models.py
Named timetables and weekly slots — class + subject + teacher + time.
"""
from django.db import models

from academics.models import ClassGroup
from schools.models import School
from subjects.models import Subject
from teachers.models import TeacherProfile


class Timetable(models.Model):

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='timetables')
    name = models.CharField(max_length=200)
    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='timetables',
        help_text='Optional — link this timetable to a class.',
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', 'name']
        unique_together = [('school', 'name')]

    def __str__(self):
        return self.name


class TimetableSlot(models.Model):
    MON, TUE, WED, THU, FRI, SAT, SUN = 0, 1, 2, 3, 4, 5, 6
    WEEKDAY_CHOICES = [
        (MON, 'Monday'), (TUE, 'Tuesday'), (WED, 'Wednesday'),
        (THU, 'Thursday'), (FRI, 'Friday'), (SAT, 'Saturday'), (SUN, 'Sunday'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='timetable_slots')
    timetable = models.ForeignKey(
        Timetable,
        on_delete=models.CASCADE,
        related_name='slots',
        null=True,
        blank=True,
    )
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='timetable_slots')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_slots')
    teacher = models.ForeignKey(
        TeacherProfile, on_delete=models.SET_NULL, null=True, related_name='timetable_slots',
    )
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=60, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f'{self.get_weekday_display()} {self.start_time} — {self.subject.name}'

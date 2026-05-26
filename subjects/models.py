"""
subjects/models.py
School-defined subjects — Hifz, Alimiyah, or General track.
"""
from django.db import models

from schools.models import School
from teachers.models import TeacherProfile


class Subject(models.Model):
    TRACK_HIFZ = 'hifz'
    TRACK_ALIMIYAH = 'alimiyah'
    TRACK_GENERAL = 'general'
    TRACK_CHOICES = [
        (TRACK_HIFZ, 'Hifz'),
        (TRACK_ALIMIYAH, 'Alimiyah'),
        (TRACK_GENERAL, 'General'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=120)
    track = models.CharField(max_length=20, choices=TRACK_CHOICES, default=TRACK_GENERAL)
    code = models.CharField(max_length=20, blank=True, help_text='Short code e.g. HIFZ-1')
    lead_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects_led',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['track', 'name']
        unique_together = [('school', 'name')]

    def __str__(self):
        return f'{self.name} ({self.get_track_display()})'

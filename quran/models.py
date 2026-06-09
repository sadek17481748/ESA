"""
quran/models.py
Per-student recitation sessions with mistake annotations and audio feedback.
"""
from django.db import models

from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile


class QuranSession(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_REVIEWED = 'reviewed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_REVIEWED, 'Reviewed'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='quran_sessions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='quran_sessions')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='quran_sessions')
    surah_number = models.PositiveSmallIntegerField()
    surah_name = models.CharField(max_length=80)
    ayah_start = models.PositiveSmallIntegerField()
    ayah_end = models.PositiveSmallIntegerField()
    ayah_text = models.TextField(help_text='Displayed mushaf text for the selected ayah range.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    student_audio = models.FileField(upload_to='quran/recitations/', blank=True)
    teacher_feedback_audio = models.FileField(upload_to='quran/feedback/', blank=True)
    teacher_notes = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.student} — {self.surah_name} ({self.ayah_start}–{self.ayah_end})'


class QuranAnnotation(models.Model):
    TAG_TAJWEED = 'tajweed'
    TAG_MEMORISATION = 'memorisation'
    TAG_FLUENCY = 'fluency'
    TAG_CHOICES = [
        (TAG_TAJWEED, 'Tajweed'),
        (TAG_MEMORISATION, 'Memorisation'),
        (TAG_FLUENCY, 'Fluency'),
    ]

    session = models.ForeignKey(QuranSession, on_delete=models.CASCADE, related_name='annotations')
    ayah_number = models.PositiveSmallIntegerField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    timestamp_seconds = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    comment = models.TextField(blank=True)
    created_by = models.ForeignKey(
        TeacherProfile, on_delete=models.SET_NULL, null=True, related_name='quran_annotations',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp_seconds', 'ayah_number']

    def __str__(self):
        return f'Ayah {self.ayah_number} — {self.get_tag_display()}'

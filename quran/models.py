"""
quran/models.py
Per-student mushaf sessions with page notes and highlights.
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
    # Legacy ayah fields — kept for older rows; new sessions use mushaf pages.
    surah_number = models.PositiveSmallIntegerField(default=1)
    surah_name = models.CharField(max_length=80, default='Mushaf')
    ayah_start = models.PositiveSmallIntegerField(default=1)
    ayah_end = models.PositiveSmallIntegerField(default=1)
    ayah_text = models.TextField(blank=True, default='')
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
        return f'{self.student} — {self.surah_name}'

    @property
    def display_title(self):
        return f'{self.student.full_name} — Mushaf session'


class QuranSessionPage(models.Model):
    """Per-page teacher notes and highlight regions for one student session."""

    session = models.ForeignKey(QuranSession, on_delete=models.CASCADE, related_name='page_markups')
    para_number = models.PositiveSmallIntegerField(help_text='Juz / para 1–30')
    page_number = models.PositiveSmallIntegerField(help_text='Page within the para PDF (1-based)')
    note = models.TextField(blank=True)
    highlights = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {x,y,w,h,color} with x/y/w/h as fractions of the page (0–1).',
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['para_number', 'page_number']
        unique_together = [('session', 'para_number', 'page_number')]

    def __str__(self):
        return f'Para {self.para_number} p{self.page_number}'


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

"""LMS — school subjects, tracks, materials, class assignments, student progress."""
from django.conf import settings
from django.db import models

from academics.models import ClassGroup
from schools.models import School
from students.models import StudentProfile


class CourseSubject(models.Model):
    """Top-level subject e.g. Maths, English."""

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='course_subjects')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = [('school', 'name')]

    def __str__(self):
        return self.name


class CourseTrack(models.Model):
    """Level within a subject e.g. Maths Foundation, Maths Higher."""

    subject = models.ForeignKey(CourseSubject, on_delete=models.CASCADE, related_name='tracks')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = [('subject', 'name')]

    def __str__(self):
        return f'{self.subject.name} — {self.name}'

    @property
    def school(self):
        return self.subject.school


class CourseMaterial(models.Model):
    TYPE_WORKSHEET = 'worksheet'
    TYPE_DOCUMENT = 'document'
    TYPE_VIDEO = 'video'
    TYPE_LINK = 'link'
    TYPE_CHOICES = [
        (TYPE_WORKSHEET, 'Worksheet'),
        (TYPE_DOCUMENT, 'Document'),
        (TYPE_VIDEO, 'Video'),
        (TYPE_LINK, 'Link'),
    ]

    track = models.ForeignKey(CourseTrack, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_WORKSHEET)
    file = models.FileField(upload_to='lms/materials/', blank=True)
    external_url = models.URLField(blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title


class ClassTrackAssignment(models.Model):
    """Teacher assigns a course track to a class."""

    class_group = models.ForeignKey(
        ClassGroup, on_delete=models.CASCADE, related_name='track_assignments',
    )
    track = models.ForeignKey(CourseTrack, on_delete=models.CASCADE, related_name='class_assignments')
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='track_assignments_made',
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('class_group', 'track')]

    def __str__(self):
        return f'{self.track} → {self.class_group.name}'


class StudentMaterialProgress(models.Model):
    STATUS_NOT_STARTED = 'not_started'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_NOT_STARTED, 'Not started'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='material_progress',
    )
    material = models.ForeignKey(
        CourseMaterial, on_delete=models.CASCADE, related_name='student_progress',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('student', 'material')]

    def __str__(self):
        return f'{self.student} — {self.material.title} ({self.progress_percent}%)'


class MaterialSubmission(models.Model):
    """Student hand-in for an LMS assignment."""

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Needs revision'),
    ]

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='material_submissions',
    )
    material = models.ForeignKey(
        CourseMaterial, on_delete=models.CASCADE, related_name='submissions',
    )
    file = models.FileField(upload_to='lms/submissions/')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    teacher_feedback = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='material_reviews',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        unique_together = [('student', 'material')]

    def __str__(self):
        return f'{self.student} — {self.material.title}'

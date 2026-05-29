"""In-house messaging — platform support and school conversations."""
from django.conf import settings
from django.db import models

from schools.models import School
from students.models import StudentProfile


class SupportCase(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]

    case_number = models.CharField(max_length=20, unique=True)
    opened_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_cases',
    )
    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.case_number} — {self.subject}'


class SupportMessage(models.Model):
    case = models.ForeignKey(SupportCase, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_messages_sent',
    )
    body = models.TextField()
    is_staff_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class SchoolConversation(models.Model):
    """School-scoped thread between parent, teacher, and school admin."""

    RECIPIENT_TEACHER = 'teacher'
    RECIPIENT_SCHOOL = 'school'
    RECIPIENT_PARENT = 'parent'
    RECIPIENT_CHOICES = [
        (RECIPIENT_TEACHER, 'Teacher'),
        (RECIPIENT_SCHOOL, 'School office'),
        (RECIPIENT_PARENT, 'Parent'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='conversations')
    subject = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_started',
    )
    recipient_type = models.CharField(max_length=20, choices=RECIPIENT_CHOICES)
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='conversations_received',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.subject


class SchoolMessage(models.Model):
    conversation = models.ForeignKey(
        SchoolConversation, on_delete=models.CASCADE, related_name='messages',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='school_messages_sent',
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class TeacherReport(models.Model):
    """Structured report from teacher to parent/student."""

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_reports')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_reports_sent',
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='teacher_reports')
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='teacher_reports_received',
    )
    subject_line = models.CharField(max_length=200, default='Progress report')
    period_covered = models.CharField(max_length=120, blank=True)
    strengths = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    action_required = models.TextField(blank=True)
    additional_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject_line} — {self.student.full_name}'

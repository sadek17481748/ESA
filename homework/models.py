"""
homework/models.py
Assignments, student submissions, and teacher sign-off.
"""
from django.conf import settings
from django.db import models

from academics.models import ClassGroup
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile


class Assignment(models.Model):
    TYPE_HOMEWORK = 'homework'
    TYPE_WORKSHEET = 'worksheet'
    TYPE_CHOICES = [
        (TYPE_HOMEWORK, 'Homework'),
        (TYPE_WORKSHEET, 'Worksheet'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='assignments')
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_HOMEWORK)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return self.title


class Submission(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='submissions')
    body = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    teacher_note = models.TextField(blank=True)
    signed_off_by = models.ForeignKey(
        TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='signoffs',
    )
    signed_off_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('assignment', 'student')]

    def __str__(self):
        return f'{self.student} — {self.assignment.title} ({self.status})'

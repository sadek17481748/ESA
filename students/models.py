"""
students/models.py
Student profile per school — may link to a User account for portal login.
"""
from django.conf import settings
from django.db import models

from schools.models import School


class StudentProfile(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile',
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    year_group = models.CharField(max_length=40, blank=True)
    admission_number = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = [('school', 'admission_number')]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class StudentLinkCode(models.Model):
    """Unique code a school issues so parents can link to this student."""

    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name='link_codes',
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='student_link_codes')
    code = models.CharField(max_length=12, unique=True, db_index=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_link_codes',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.code} → {self.student}'

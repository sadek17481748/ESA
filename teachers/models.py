"""
teachers/models.py
Links a User (teacher role) to a school with subject and employee code.
"""
from django.conf import settings
from django.db import models

from schools.models import School


class TeacherProfile(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
    )
    subject = models.CharField(max_length=120, blank=True)
    employee_code = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

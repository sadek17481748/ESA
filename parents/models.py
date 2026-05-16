"""
parents/models.py
Parent accounts linked to children at the same school.
"""
from django.conf import settings
from django.db import models

from schools.models import School


class ParentProfile(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='parents')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parent_profile',
    )
    phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__last_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class StudentParentLink(models.Model):
    """Which students belong to which parent."""

    REL_MOTHER = 'mother'
    REL_FATHER = 'father'
    REL_GUARDIAN = 'guardian'
    REL_CHOICES = [
        (REL_MOTHER, 'Mother'),
        (REL_FATHER, 'Father'),
        (REL_GUARDIAN, 'Guardian'),
    ]

    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children_links')
    student = models.ForeignKey(
        'students.StudentProfile', on_delete=models.CASCADE, related_name='parent_links',
    )
    relationship = models.CharField(max_length=20, choices=REL_CHOICES, default=REL_GUARDIAN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('parent', 'student')]

    def __str__(self):
        return f'{self.parent} → {self.student}'

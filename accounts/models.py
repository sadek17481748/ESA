from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('school_admin', 'School Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    school = models.ForeignKey(
        'schools.School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        help_text='Tenant school — blank for super admin only',
    )

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

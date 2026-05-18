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

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.role == 'super_admin' and self.school_id:
            raise ValidationError({'school': 'Super admin cannot belong to a school.'})
        if self.role != 'super_admin' and not self.school_id:
            raise ValidationError({'school': 'This role must be linked to a school.'})

    def save(self, *args, **kwargs):
        if self.role == 'super_admin':
            self.school = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

# bug: super_admin with a school set caused 500 on save — school FK was required for all roles

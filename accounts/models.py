"""
accounts/models.py
Custom user model for ESA — every login has a role and (usually) a school tenant.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extends Django user with ESA role and optional school FK."""

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('school_admin', 'School Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    # drives RBAC checks in core_app.permissions and API view permissions
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
        """Admin/forms validation — super admin must not have a school."""
        from django.core.exceptions import ValidationError
        if self.role == 'super_admin' and self.school_id:
            raise ValidationError({'school': 'Super admin cannot belong to a school.'})
        if self.role != 'super_admin' and not self.school_id:
            raise ValidationError({'school': 'This role must be linked to a school.'})

    def save(self, *args, **kwargs):
        # strip school on save so super_admin row stays clean
        if self.role == 'super_admin':
            self.school = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    notify_on_messages = models.BooleanField(
        default=True,
        help_text='Send email when a new school message reply arrives.',
    )
    email_verified = models.BooleanField(
        default=False,
        help_text='True after the user confirms their email with a verification code.',
    )


class EmailVerificationCode(models.Model):
    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='email_codes',
    )
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.code}'

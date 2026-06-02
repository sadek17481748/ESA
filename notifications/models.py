"""
notifications/models.py
In-app notifications — assignments due, sign-off results, etc.
"""
from django.conf import settings
from django.db import models

from schools.models import School


class Notification(models.Model):
    TYPE_ASSIGNMENT = 'assignment'
    TYPE_SIGNOFF = 'signoff'
    TYPE_ATTENDANCE = 'attendance'
    TYPE_GENERAL = 'general'
    TYPE_CHOICES = [
        (TYPE_ASSIGNMENT, 'Assignment'),
        (TYPE_SIGNOFF, 'Sign-off'),
        (TYPE_ATTENDANCE, 'Attendance'),
        (TYPE_GENERAL, 'General'),
    ]

    school = models.ForeignKey(
        School, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications',
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_GENERAL)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link_path = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.user.username}'

"""notifications/services.py — create in-app notification rows."""
from .models import Notification


def notify_user(*, user, school, notification_type, title, message, link_path=''):
    return Notification.objects.create(
        user=user,
        school=school,
        notification_type=notification_type,
        title=title,
        message=message,
        link_path=link_path,
    )

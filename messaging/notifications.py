"""Email alerts when a school message is sent."""
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .models import SchoolConversation
from .unread import conversation_recipients_excluding_sender


def notify_school_message_recipients(message):
    """Email other participants when notify_on_messages is enabled."""
    conv = message.conversation
    recipients = conversation_recipients_excluding_sender(conv, message.sender)
    if not recipients:
        return

    sender_name = message.sender.get_full_name() or message.sender.username
    subject = f'New message: {conv.subject}'
    try:
        inbox_path = reverse('messaging:school_detail', args=[conv.pk])
    except Exception:
        inbox_path = '/messages/'

    for user in recipients:
        if not getattr(user, 'notify_on_messages', True):
            continue
        if not user.email:
            continue
        body = (
            f'Salam {user.get_full_name() or user.username},\n\n'
            f'{sender_name} replied in "{conv.subject}":\n\n'
            f'{message.body[:500]}\n\n'
            f'Log in to read and reply.\n'
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

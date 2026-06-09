"""Central email helpers — platform inbox and user notifications."""
from django.conf import settings
from django.core.mail import EmailMessage, send_mail


def email_is_configured():
    """True when SMTP credentials are set (Gmail app password, etc.)."""
    return bool(getattr(settings, 'EMAIL_HOST_USER', '') and settings.EMAIL_HOST_PASSWORD)


def platform_inbox():
    return getattr(settings, 'ESA_PLATFORM_EMAIL', 'educationandschoolapplications@gmail.com')


def send_platform_email(subject, body, *, reply_to=None):
    """
    Send a copy to the ESA platform Gmail inbox.
    Used for subscriptions, school messages, support tickets, registrations.
    """
    if not email_is_configured():
        return False
    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[platform_inbox()],
    )
    if reply_to:
        msg.reply_to = [reply_to]
    msg.send(fail_silently=False)
    return True


def send_user_email(subject, body, recipients):
    """Send to one or more user email addresses."""
    recipients = [r for r in recipients if r]
    if not recipients or not email_is_configured():
        return False
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=True,
    )
    return True

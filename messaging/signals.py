"""Send email when school or support messages are created."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SchoolMessage, SupportMessage
from .notifications import notify_platform_support_message, notify_school_message_recipients


@receiver(post_save, sender=SchoolMessage)
def email_on_school_message(sender, instance, created, **kwargs):
    if created:
        notify_school_message_recipients(instance)


@receiver(post_save, sender=SupportMessage)
def email_on_support_message(sender, instance, created, **kwargs):
    if created:
        notify_platform_support_message(instance)

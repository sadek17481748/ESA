"""Send email when school messages are created."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import SchoolMessage
from .notifications import notify_school_message_recipients


@receiver(post_save, sender=SchoolMessage)
def email_on_school_message(sender, instance, created, **kwargs):
    if created:
        notify_school_message_recipients(instance)

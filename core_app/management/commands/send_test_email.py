"""Send a test email to the platform inbox — verifies Gmail SMTP setup."""
from django.core.management.base import BaseCommand

from core_app.email_service import email_is_configured, platform_inbox, send_platform_email


class Command(BaseCommand):
    help = 'Send a test email to ESA_PLATFORM_EMAIL (Gmail SMTP must be configured)'

    def handle(self, *args, **options):
        if not email_is_configured():
            self.stdout.write(self.style.ERROR(
                'Email not configured. Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env '
                '(use a Gmail App Password for educationandschoolapplications@gmail.com).'
            ))
            return

        inbox = platform_inbox()
        send_platform_email(
            '[ESA] Test email',
            f'This is a test from the ESA Django app.\n\nPlatform inbox: {inbox}\n',
        )
        self.stdout.write(self.style.SUCCESS(f'Test email sent to {inbox}'))

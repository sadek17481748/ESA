"""Management command: mark overdue fees and email/notify parents."""
from django.core.management.base import BaseCommand

from payments.overdue import process_overdue_reminders


class Command(BaseCommand):
    help = 'Mark past-due fees as overdue and send parent email + in-app reminders'

    def handle(self, *args, **options):
        fees = process_overdue_reminders()
        self.stdout.write(self.style.SUCCESS(f'Processed {len(fees)} overdue fee(s).'))

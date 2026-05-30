"""
Ensure at least one school exists for web registration.
Run on Heroku release / web boot when using SQLite.
"""
from django.core.management.base import BaseCommand

from schools.models import School


class Command(BaseCommand):
    help = 'Creates demo school if the database has no schools yet'

    def handle(self, *args, **options):
        school, created = School.objects.get_or_create(
            name='Al-Noor Academy',
            defaults={'contact_email': 'admin@alnoor.example'},
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Al-Noor Academy'))
        else:
            self.stdout.write('School already exists')

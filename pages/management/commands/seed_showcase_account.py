"""
Create one showcase student + parent with attendance, behaviour, reports, fees, and more.

Run: python manage.py seed_showcase_account
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from schools.models import School

from pages.showcase_seed import (
    SHOWCASE_CLASS,
    SHOWCASE_PARENT_USERNAME,
    SHOWCASE_PASSWORD,
    SHOWCASE_STUDENT_USERNAME,
    seed_showcase_account,
)

SCHOOL_NAME = 'Al-Noor Academy'


class Command(BaseCommand):
    help = 'Seeds demo_student / demo_parent — one account with full portal data'

    def handle(self, *args, **options):
        school = School.objects.filter(name=SCHOOL_NAME).first()
        if not school:
            call_command('ensure_platform_seed')
            school = School.objects.filter(name=SCHOOL_NAME).first()
        if not school:
            raise CommandError('Al-Noor Academy not found.')

        from academics.models import ClassGroup

        if not ClassGroup.objects.filter(school=school, name=SHOWCASE_CLASS).exists():
            self.stdout.write(f'  {SHOWCASE_CLASS} missing — running full school seed…')
            call_command('seed_alnoor_full_school')

        from pages.seed_helpers import sync_mr_mohammed_attendance_demo

        sync_mr_mohammed_attendance_demo(school, stdout=self.stdout)
        seed_showcase_account(school, stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS('\nShowcase logins (Al-Noor Academy, class 7A):\n'))
        self.stdout.write(f'  Student: {SHOWCASE_STUDENT_USERNAME} / {SHOWCASE_PASSWORD}')
        self.stdout.write(f'  Parent:  {SHOWCASE_PARENT_USERNAME} / {SHOWCASE_PASSWORD}')
        self.stdout.write('\n  Teacher (mark attendance, sign-offs): mr_mohammed / teacher1234')
        self.stdout.write('  Live: https://esa-project-2a7a33dfe3fc.herokuapp.com/accounts/login/\n')

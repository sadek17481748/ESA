"""
Full Al-Noor Academy — structure + rich content (homework, exams, Quran, LMS,
attendance, behaviour, messages, fees, sign-offs).

Run once on Postgres:
  python manage.py seed_alnoor_comprehensive

Re-runnable and idempotent.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand

from schools.models import School

from pages.alnoor_content_seed import seed_alnoor_rich_content
from pages.seed_helpers import (
    PERSONAL_PARENT_EMAIL,
    PERSONAL_PARENT_PASSWORD,
    PERSONAL_TEACHER_EMAIL,
    PERSONAL_TEACHER_PASSWORD,
    sync_mr_mohammed_attendance_demo,
    sync_personal_accounts,
)

SCHOOL_NAME = 'Al-Noor Academy'


class Command(BaseCommand):
    help = 'Seed Al-Noor Academy with full structure and functioning school content'

    def handle(self, *args, **options):
        self.stdout.write('Phase 1 — platform boot accounts…')
        call_command('ensure_platform_seed')

        self.stdout.write('Phase 2 — school structure (classes, users, timetables)…')
        call_command('seed_alnoor_full_school')

        school = School.objects.get(name=SCHOOL_NAME)
        self.stdout.write('Phase 3 — rich content (homework, exams, Quran, messages…)…')
        seed_alnoor_rich_content(school, stdout=self.stdout)

        sync_personal_accounts(school, stdout=self.stdout)
        sync_mr_mohammed_attendance_demo(school, stdout=self.stdout)

        self.stdout.write(self.style.SUCCESS(
            '\nAl-Noor Academy is fully seeded.\n'
            'Full login CSV: docs/alnoor-academy-logins.csv\n\n'
            'Staff logins:\n'
            '  schooladmin / admin1234\n'
            '  super / super1234\n'
            '  mr_mohammed / teacher1234\n'
            '  ms_fatima_s{n} / teacher1234  (Quran — check CSV for exact username)\n'
            '  mr_ali_s{n} / teacher1234     (Maths)\n'
            '  mr_yusuf_s{n} / teacher1234   (Arabic)\n'
            f'  {PERSONAL_TEACHER_EMAIL} / {PERSONAL_TEACHER_PASSWORD}\n'
            f'  {PERSONAL_PARENT_EMAIL} / {PERSONAL_PARENT_PASSWORD}\n\n'
            'Bulk pattern (all 10 classes, 30 students each):\n'
            '  student_{class}_{nn} / student1234  e.g. student_7a_01\n'
            '  parent_{class}_{nn} / parent1234    e.g. parent_7a_01 (linked guardian)\n'
            '  Classes: 7A 7B 8A 8B 9A 9B 10A 10B 11A 11B\n'
        ))

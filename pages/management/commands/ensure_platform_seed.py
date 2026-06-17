"""
Ensure demo school and login accounts exist (Heroku / fresh DB).
Fast boot path only — heavy seeding is manual: python manage.py seed_alnoor_full_school
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parents.models import ParentProfile
from schools.models import School

from pages.seed_helpers import (
    PUBLIC_DEMO_USERNAMES,
    sync_mr_mohammed_attendance_demo,
    sync_personal_accounts,
    upsert_user,
)

User = get_user_model()

DEMO_SCHOOL_NAME = 'Al-Noor Academy'

DEMO_LOGINS = (
    ('schooladmin', 'school_admin', 'admin1234', 'School', 'Admin', 'admin@alnoor.example'),
    ('parent_demo', 'parent', 'demo1234', 'Parent', 'Demo', 'parent@alnoor.example'),
)


class Command(BaseCommand):
    help = 'Fast boot seed — demo logins + personal accounts only (no bulk school seed)'

    def handle(self, *args, **options):
        school, school_created = School.objects.get_or_create(
            name=DEMO_SCHOOL_NAME,
            defaults={'contact_email': 'admin@alnoor.example'},
        )
        if school_created:
            self.stdout.write(self.style.SUCCESS(f'Created {DEMO_SCHOOL_NAME}'))
        else:
            self.stdout.write(f'School exists: {DEMO_SCHOOL_NAME}')

        for username, role, password, first, last, email in DEMO_LOGINS:
            user, created = upsert_user(
                username,
                email=email,
                role=role,
                password=password,
                school=school,
                first_name=first,
                last_name=last,
                force_reset_password=username in PUBLIC_DEMO_USERNAMES,
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {username} ({role})')
            if role == 'parent':
                ParentProfile.objects.get_or_create(
                    user=user,
                    defaults={'school': school},
                )

        super_user, super_created = upsert_user(
            'super',
            email='super@esa.demo',
            role='super_admin',
            password='super1234',
            school=None,
            first_name='Super',
            last_name='Admin',
            force_reset_password=True,
        )
        self.stdout.write(f"{'Created' if super_created else 'Updated'} super (super_admin)")

        sync_personal_accounts(school, stdout=self.stdout)
        sync_mr_mohammed_attendance_demo(school, stdout=self.stdout)

        from django.core.management import call_command
        call_command('seed_rbac_users', verbosity=0)

        self.stdout.write(self.style.SUCCESS(
            'Boot seed complete (fast). For full Y7–Y11 data run: '
            'python manage.py seed_alnoor_full_school'
        ))

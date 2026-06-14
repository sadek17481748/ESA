"""
Ensure demo school and login accounts exist (Heroku / fresh DB).
Preserves user passwords and data across deploys — only resets public demo logins.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parents.models import ParentProfile
from schools.models import School

from pages.seed_helpers import PUBLIC_DEMO_USERNAMES, upsert_user

User = get_user_model()

DEMO_SCHOOL_NAME = 'Al-Noor Academy'

# username, role, password, first_name, last_name, email
DEMO_LOGINS = (
    ('schooladmin', 'school_admin', 'admin1234', 'School', 'Admin', 'admin@alnoor.example'),
    ('parent_demo', 'parent', 'demo1234', 'Parent', 'Demo', 'parent@alnoor.example'),
)


class Command(BaseCommand):
    help = 'Seeds Al-Noor Academy — idempotent, preserves registered accounts on deploy'

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

        from django.core.management import call_command
        from students.models import StudentProfile

        if StudentProfile.objects.filter(school=school, admission_number='Y7A-001').exists():
            self.stdout.write('Full school already seeded — syncing personal accounts.')
        call_command('seed_alnoor_full_school')
        call_command('seed_alnoor_examples')

        self.stdout.write(self.style.SUCCESS(
            'Demo logins — super / super1234 · schooladmin / admin1234 · '
            'parent_demo / demo1234 · msadekhussain@outlook.com / Parent2026! · '
            'msadekhussain2001@gmail.com / Teacher2026!'
        ))

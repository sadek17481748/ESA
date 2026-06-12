"""
Ensure demo school and login accounts exist (Heroku / fresh DB).
Creates Al-Noor Academy plus schooladmin and parent_demo — passwords reset each run.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parents.models import ParentProfile
from schools.models import School

User = get_user_model()

DEMO_SCHOOL_NAME = 'Al-Noor Academy'

# username, role, password, first_name, last_name, email
DEMO_LOGINS = (
    ('schooladmin', 'school_admin', 'admin1234', 'School', 'Admin', 'admin@alnoor.example'),
    ('parent_demo', 'parent', 'demo1234', 'Parent', 'Demo', 'parent@alnoor.example'),
)


class Command(BaseCommand):
    help = 'Seeds Al-Noor Academy and demo school admin + parent logins'

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
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email},
            )
            user.email = email
            user.first_name = first
            user.last_name = last
            user.role = role
            user.school = school
            user.set_password(password)
            user.is_active = True
            user.email_verified = True
            user.save()
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} {username} ({role})')

            if role == 'parent':
                ParentProfile.objects.get_or_create(
                    user=user,
                    defaults={'school': school},
                )

        super_user, super_created = User.objects.get_or_create(
            username='super',
            defaults={'email': 'super@esa.demo'},
        )
        super_user.email = 'super@esa.demo'
        super_user.first_name = 'Super'
        super_user.last_name = 'Admin'
        super_user.role = 'super_admin'
        super_user.school = None
        super_user.set_password('super1234')
        super_user.is_active = True
        super_user.email_verified = True
        super_user.save()
        self.stdout.write(f"{'Created' if super_created else 'Updated'} super (super_admin)")

        self.stdout.write(self.style.SUCCESS(
            'Demo logins — super / super1234 · schooladmin / admin1234 · parent_demo / demo1234'
        ))

        from django.core.management import call_command
        call_command('seed_alnoor_demo')
        call_command('seed_alnoor_examples')
        # Demo timetable data for the registered school-admin school (not Al-Noor)
        call_command('seed_timetable_samples')

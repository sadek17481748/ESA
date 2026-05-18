from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates demo users for each ESA role (RBAC testing)'

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(
            name='Al-Noor Academy',
            defaults={'contact_email': 'admin@alnoor.example'},
        )

        users_spec = [
            ('super_admin', 'super', None, 'super1234'),
            ('school_admin', 'schooladmin', school, 'admin1234'),
            ('teacher', 'teacher_demo', school, 'teacher1234'),
            ('student', 'student_demo', school, 'student1234'),
            ('parent', 'parent_demo', school, 'demo1234'),
        ]

        for role, username, user_school, password in users_spec:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@esa.demo',
                    'role': role,
                    'school': user_school,
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'Created {username} ({role})')
            else:
                self.stdout.write(f'Exists {username}')

        teacher_user = User.objects.get(username='teacher_demo')
        TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={'school': school, 'subject': 'Quran'},
        )

        student_user = User.objects.get(username='student_demo')
        StudentProfile.objects.get_or_create(
            school=school,
            admission_number='ESA001',
            defaults={
                'user': student_user,
                'first_name': 'Ahmed',
                'last_name': 'Hussain',
                'year_group': 'Year 7',
            },
        )

        self.stdout.write(self.style.SUCCESS('RBAC seed complete — see README for passwords'))

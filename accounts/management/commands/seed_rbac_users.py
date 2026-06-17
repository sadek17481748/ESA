"""
Management command: seed_rbac_users
Creates one demo user per ESA role plus sample teacher/student profiles.
Run: python manage.py seed_rbac_users
"""
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

        # role, username, school (None for super), password
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
            user.email_verified = True
            if created:
                user.set_password(password)
                self.stdout.write(f'Created {username} ({role})')
            else:
                self.stdout.write(f'Exists {username}')
            user.save()

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

        parent_user = User.objects.get(username='parent_demo')
        from parents.models import ParentProfile, StudentParentLink
        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            defaults={'school': school, 'phone': '07700900000'},
        )
        student = StudentProfile.objects.get(admission_number='ESA001', school=school)
        StudentParentLink.objects.get_or_create(
            parent=parent_profile,
            student=student,
            defaults={'relationship': 'father'},
        )

        from academics.models import ClassEnrollment, ClassGroup, YearGroup
        y7, _ = YearGroup.objects.get_or_create(
            school=school, name='Year 7', defaults={'sort_order': 7},
        )
        class_7a, _ = ClassGroup.objects.get_or_create(
            school=school, name='7A',
            defaults={'year_group': y7, 'teacher': TeacherProfile.objects.get(user=teacher_user)},
        )
        ClassEnrollment.objects.get_or_create(class_group=class_7a, student=student)

        from subjects.models import Subject
        Subject.objects.get_or_create(
            school=school, name='Quran — Hifz',
            defaults={
                'track': 'hifz',
                'code': 'HIFZ-1',
                'lead_teacher': TeacherProfile.objects.get(user=teacher_user),
            },
        )
        Subject.objects.get_or_create(
            school=school, name='Islamic Studies',
            defaults={'track': 'general', 'code': 'IS-1'},
        )

        self.stdout.write(self.style.SUCCESS('RBAC seed complete — see README for passwords'))

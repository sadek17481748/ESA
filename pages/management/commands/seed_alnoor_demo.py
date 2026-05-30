"""
Seed Al-Noor Academy demo class — 30 students, 30 parents, subjects, Year 7.
Run: python manage.py seed_alnoor_demo
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academics.models import ClassEnrollment, ClassGroup, YearGroup
from parents.models import ParentProfile, StudentParentLink
from payments.models import FeeItem
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

from pages.timetable_service import ensure_school_subjects, get_or_create_default_timetable

User = get_user_model()

SCHOOL_NAME = 'Al-Noor Academy'


class Command(BaseCommand):
    help = 'Seeds Year 7 class with 30 students, 30 parents, and Mr Mohammed teacher'

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(
            name=SCHOOL_NAME,
            defaults={'contact_email': 'admin@alnoor.example'},
        )
        ensure_school_subjects(school)

        teacher_user, _ = User.objects.get_or_create(
            username='mr_mohammed',
            defaults={'email': 'mohammed@alnoor.example'},
        )
        teacher_user.email = 'mohammed@alnoor.example'
        teacher_user.first_name = 'Mohammed'
        teacher_user.last_name = 'Hussain'
        teacher_user.role = 'teacher'
        teacher_user.school = school
        teacher_user.set_password('teacher1234')
        teacher_user.is_active = True
        teacher_user.save()

        teacher_profile, _ = TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={'school': school, 'subject': 'Quran'},
        )
        teacher_profile.school = school
        teacher_profile.subject = 'Quran'
        teacher_profile.save()

        y7, _ = YearGroup.objects.get_or_create(
            school=school, name='Year 7', defaults={'sort_order': 7},
        )
        class_7a, _ = ClassGroup.objects.get_or_create(
            school=school,
            name='Year 7',
            defaults={'year_group': y7, 'teacher': teacher_profile},
        )
        class_7a.year_group = y7
        class_7a.teacher = teacher_profile
        class_7a.save()

        get_or_create_default_timetable(school, class_7a)

        for i in range(1, 31):
            uname = f'parent_alnoor_{i:02d}'
            parent_user, created = User.objects.get_or_create(
                username=uname,
                defaults={'email': f'parent{i}@alnoor.example'},
            )
            parent_user.email = f'parent{i}@alnoor.example'
            parent_user.first_name = 'Parent'
            parent_user.last_name = f'Family {i}'
            parent_user.role = 'parent'
            parent_user.school = school
            parent_user.set_password('parent1234')
            parent_user.is_active = True
            parent_user.save()

            parent_profile, _ = ParentProfile.objects.get_or_create(
                user=parent_user,
                defaults={'school': school},
            )

            student_uname = f'student_alnoor_{i:02d}'
            student_user, _ = User.objects.get_or_create(
                username=student_uname,
                defaults={'email': f'student{i}@alnoor.example'},
            )
            student_user.email = f'student{i}@alnoor.example'
            student_user.first_name = f'Student'
            student_user.last_name = f'Al-Noor {i}'
            student_user.role = 'student'
            student_user.school = school
            student_user.set_password('student1234')
            student_user.is_active = True
            student_user.save()

            student_profile, _ = StudentProfile.objects.get_or_create(
                user=student_user,
                defaults={
                    'school': school,
                    'first_name': student_user.first_name,
                    'last_name': student_user.last_name,
                    'year_group': 'Year 7',
                    'admission_number': f'AN{i:03d}',
                },
            )
            student_profile.school = school
            student_profile.year_group = 'Year 7'
            student_profile.admission_number = f'AN{i:03d}'
            student_profile.save()

            StudentParentLink.objects.get_or_create(
                parent=parent_profile,
                student=student_profile,
                defaults={'relationship': 'guardian'},
            )
            ClassEnrollment.objects.get_or_create(
                class_group=class_7a,
                student=student_profile,
            )

        if not FeeItem.objects.filter(school=school, title='Term 1 tuition').exists():
            for i in range(1, 31):
                parent_user = User.objects.get(username=f'parent_alnoor_{i:02d}')
                student_profile = StudentProfile.objects.get(
                    user__username=f'student_alnoor_{i:02d}',
                )
                child_name = f'{student_profile.first_name} {student_profile.last_name}'.strip()
                if i <= 10:
                    status = FeeItem.STATUS_PAID
                    due = date.today() + timedelta(days=30)
                elif i <= 20:
                    status = FeeItem.STATUS_OUTSTANDING
                    due = date.today() + timedelta(days=14)
                else:
                    status = FeeItem.STATUS_OVERDUE
                    due = date.today() - timedelta(days=7)
                FeeItem.objects.create(
                    school=school,
                    parent=parent_user,
                    child_name=child_name,
                    title='Term 1 tuition',
                    amount_pence=25000,
                    due_date=due,
                    status=status,
                )

        from lms.models import ClassTrackAssignment, CourseMaterial, CourseSubject, CourseTrack

        maths, _ = CourseSubject.objects.get_or_create(
            school=school,
            name='Maths',
            defaults={'description': 'Mathematics curriculum'},
        )
        foundation, _ = CourseTrack.objects.get_or_create(
            subject=maths,
            name='Foundation',
            defaults={'sort_order': 0},
        )
        higher, _ = CourseTrack.objects.get_or_create(
            subject=maths,
            name='Higher',
            defaults={'sort_order': 1},
        )
        CourseMaterial.objects.get_or_create(
            track=foundation,
            title='Number basics worksheet',
            defaults={
                'material_type': CourseMaterial.TYPE_LINK,
                'external_url': 'https://example.com/maths-foundation-1',
            },
        )
        CourseMaterial.objects.get_or_create(
            track=higher,
            title='Algebra challenge',
            defaults={
                'material_type': CourseMaterial.TYPE_LINK,
                'external_url': 'https://example.com/maths-higher-1',
            },
        )
        ClassTrackAssignment.objects.get_or_create(
            class_group=class_7a,
            track=foundation,
            defaults={'assigned_by': teacher_user},
        )

        self.stdout.write(self.style.SUCCESS(
            'Al-Noor demo: Year 7 (Mr Mohammed), 30 students, 30 parents — '
            'mr_mohammed/teacher1234 · test_parent/test1234 · test_student/test1234'
        ))

"""
Seed working examples for messaging and LMS — test_parent / test_student at Al-Noor.
Run: python manage.py seed_alnoor_examples
Use mr_mohammed to exercise teacher flows; test_parent and test_student for family flows.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from academics.models import ClassEnrollment, ClassGroup
from lms.models import (
    ClassTrackAssignment,
    CourseMaterial,
    CourseSubject,
    CourseTrack,
    StudentMaterialProgress,
)
from messaging.models import (
    SchoolConversation,
    SchoolMessage,
    SupportCase,
    SupportMessage,
    TeacherReport,
)
from parents.models import ParentProfile, StudentParentLink
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()

SCHOOL_NAME = 'Al-Noor Academy'
TEST_PARENT_USERNAME = 'test_parent'
TEST_STUDENT_USERNAME = 'test_student'
TEST_PASSWORD = 'test1234'


class Command(BaseCommand):
    help = 'Seeds test_parent/test_student with messaging, LMS, and report examples'

    def handle(self, *args, **options):
        from django.core.management import call_command

        if not User.objects.filter(username='mr_mohammed').exists():
            call_command('seed_alnoor_demo')

        school = School.objects.get(name=SCHOOL_NAME)
        teacher_user = User.objects.get(username='mr_mohammed')
        teacher_profile = TeacherProfile.objects.get(user=teacher_user)
        class_group = ClassGroup.objects.get(school=school, name='Year 7')
        super_user = User.objects.filter(username='super', role='super_admin').first()
        school_admin = User.objects.filter(username='schooladmin', school=school).first()

        parent_user, _ = User.objects.get_or_create(
            username=TEST_PARENT_USERNAME,
            defaults={'email': 'fatima.hassan@alnoor.example'},
        )
        parent_user.email = 'fatima.hassan@alnoor.example'
        parent_user.first_name = 'Fatima'
        parent_user.last_name = 'Hassan'
        parent_user.role = 'parent'
        parent_user.school = school
        parent_user.set_password(TEST_PASSWORD)
        parent_user.is_active = True
        parent_user.save()

        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            defaults={'school': school},
        )

        student_user, _ = User.objects.get_or_create(
            username=TEST_STUDENT_USERNAME,
            defaults={'email': 'amina.hassan@alnoor.example'},
        )
        student_user.email = 'amina.hassan@alnoor.example'
        student_user.first_name = 'Amina'
        student_user.last_name = 'Hassan'
        student_user.role = 'student'
        student_user.school = school
        student_user.set_password(TEST_PASSWORD)
        student_user.is_active = True
        student_user.save()

        student_profile, _ = StudentProfile.objects.get_or_create(
            user=student_user,
            defaults={
                'school': school,
                'first_name': 'Amina',
                'last_name': 'Hassan',
                'year_group': 'Year 7',
                'admission_number': 'AN-TEST',
            },
        )
        student_profile.school = school
        student_profile.first_name = 'Amina'
        student_profile.last_name = 'Hassan'
        student_profile.year_group = 'Year 7'
        student_profile.admission_number = 'AN-TEST'
        student_profile.save()

        StudentParentLink.objects.get_or_create(
            parent=parent_profile,
            student=student_profile,
            defaults={'relationship': 'mother'},
        )
        ClassEnrollment.objects.get_or_create(
            class_group=class_group,
            student=student_profile,
        )

        self._seed_support(parent_user, super_user)
        self._seed_school_messages(school, parent_user, teacher_user, school_admin)
        self._seed_teacher_report(school, teacher_user, student_profile, parent_user)
        self._seed_lms(school, class_group, teacher_user, student_profile)

        self.stdout.write(self.style.SUCCESS(
            'Demo examples ready — test_parent / test1234 · test_student / test1234 · '
            'mr_mohammed / teacher1234 (teacher flows)'
        ))

    def _seed_support(self, parent_user, super_user):
        case, created = SupportCase.objects.get_or_create(
            case_number='ESA-00001',
            defaults={
                'opened_by': parent_user,
                'subject': 'Cannot see homework on mobile',
                'status': SupportCase.STATUS_OPEN,
            },
        )
        if created or not case.messages.exists():
            SupportMessage.objects.get_or_create(
                case=case,
                sender=parent_user,
                defaults={
                    'body': (
                        'Salam, I logged in as test_parent on my phone but the homework '
                        'page looks empty. Works fine on laptop.'
                    ),
                },
            )
            if super_user:
                SupportMessage.objects.get_or_create(
                    case=case,
                    sender=super_user,
                    defaults={
                        'body': (
                            'Thank you for reporting this. We have reproduced the issue on '
                            'mobile and are rolling out a fix. Your case remains open until confirmed.'
                        ),
                        'is_staff_reply': True,
                    },
                )

        SupportCase.objects.get_or_create(
            case_number='ESA-00002',
            defaults={
                'opened_by': parent_user,
                'subject': 'Request invoice copy for Term 1',
                'status': SupportCase.STATUS_CLOSED,
            },
        )

    def _seed_school_messages(self, school, parent_user, teacher_user, school_admin):
        conv_teacher, created = SchoolConversation.objects.get_or_create(
            school=school,
            subject='Question about maths worksheet',
            created_by=parent_user,
            recipient_type=SchoolConversation.RECIPIENT_TEACHER,
            recipient_user=teacher_user,
            defaults={'created_by': parent_user},
        )
        if created or conv_teacher.messages.count() < 2:
            SchoolMessage.objects.get_or_create(
                conversation=conv_teacher,
                sender=parent_user,
                defaults={
                    'body': 'As-salamu alaykum Mr Mohammed — should Amina show working for question 4?',
                },
            )
            SchoolMessage.objects.get_or_create(
                conversation=conv_teacher,
                sender=teacher_user,
                defaults={
                    'body': 'Wa alaykum salam — yes please, even if the final answer is correct.',
                },
            )

        conv_parent, created = SchoolConversation.objects.get_or_create(
            school=school,
            subject='Well done certificate',
            created_by=teacher_user,
            recipient_type=SchoolConversation.RECIPIENT_PARENT,
            recipient_user=parent_user,
            defaults={'created_by': teacher_user},
        )
        if created or conv_parent.messages.count() < 1:
            SchoolMessage.objects.get_or_create(
                conversation=conv_parent,
                sender=teacher_user,
                defaults={
                    'body': 'Amina earned the class star this week for excellent participation in Quran.',
                },
            )

        if school_admin:
            conv_office, created = SchoolConversation.objects.get_or_create(
                school=school,
                subject='After-school club registration',
                created_by=parent_user,
                recipient_type=SchoolConversation.RECIPIENT_SCHOOL,
                defaults={'created_by': parent_user},
            )
            if created or conv_office.messages.count() < 2:
                SchoolMessage.objects.get_or_create(
                    conversation=conv_office,
                    sender=parent_user,
                    defaults={
                        'body': 'Please confirm Amina is registered for the Saturday Arabic club.',
                    },
                )
                SchoolMessage.objects.get_or_create(
                    conversation=conv_office,
                    sender=school_admin,
                    defaults={
                        'body': 'Confirmed — Amina is on the register. First session is next Saturday 10am.',
                    },
                )

    def _seed_teacher_report(self, school, teacher_user, student_profile, parent_user):
        TeacherReport.objects.get_or_create(
            school=school,
            teacher=teacher_user,
            student=student_profile,
            subject_line='Spring term progress — Amina Hassan',
            defaults={
                'parent': parent_user,
                'period_covered': 'Spring term 2026',
                'strengths': 'Confident reader, participates well in class discussions.',
                'areas_for_improvement': 'Practice times tables 6–12 for five minutes daily.',
                'action_required': 'Please sign the reading log each week.',
                'additional_notes': 'Happy to discuss at parents evening.',
            },
        )

    def _seed_lms(self, school, class_group, teacher_user, student_profile):
        maths, _ = CourseSubject.objects.get_or_create(
            school=school,
            name='Maths',
            defaults={'description': 'Mathematics curriculum for Year 7'},
        )
        foundation, _ = CourseTrack.objects.get_or_create(
            subject=maths,
            name='Foundation',
            defaults={'description': 'Core number and algebra skills', 'sort_order': 0},
        )
        higher, _ = CourseTrack.objects.get_or_create(
            subject=maths,
            name='Higher',
            defaults={'description': 'Extended problem solving', 'sort_order': 1},
        )

        english, _ = CourseSubject.objects.get_or_create(
            school=school,
            name='English',
            defaults={'description': 'Reading, writing, and comprehension'},
        )
        english_core, _ = CourseTrack.objects.get_or_create(
            subject=english,
            name='Foundation',
            defaults={'sort_order': 0},
        )

        quran, _ = CourseSubject.objects.get_or_create(
            school=school,
            name='Quran',
            defaults={'description': 'Tajweed and memorisation support'},
        )
        quran_beginners, _ = CourseTrack.objects.get_or_create(
            subject=quran,
            name='Beginners',
            defaults={'sort_order': 0},
        )

        foundation_materials = [
            ('Number basics — place value', CourseMaterial.TYPE_LINK, 'https://example.com/maths-foundation-1', 0),
            ('Fractions worksheet', CourseMaterial.TYPE_LINK, 'https://example.com/maths-foundation-2', 1),
            ('Weekly arithmetic quiz', CourseMaterial.TYPE_DOCUMENT, '', 2),
        ]
        for title, mtype, url, order in foundation_materials:
            CourseMaterial.objects.get_or_create(
                track=foundation,
                title=title,
                defaults={
                    'material_type': mtype,
                    'external_url': url,
                    'sort_order': order,
                    'description': 'Year 7 Foundation maths',
                },
            )

        for title, url in [
            ('Algebra introduction', 'https://example.com/maths-higher-1'),
            ('Problem solving set B', 'https://example.com/maths-higher-2'),
        ]:
            CourseMaterial.objects.get_or_create(
                track=higher,
                title=title,
                defaults={
                    'material_type': CourseMaterial.TYPE_LINK,
                    'external_url': url,
                },
            )

        for title in ('Reading comprehension — Surah Al-Asr', 'Creative writing: my community'):
            CourseMaterial.objects.get_or_create(
                track=english_core,
                title=title,
                defaults={
                    'material_type': CourseMaterial.TYPE_LINK,
                    'external_url': 'https://example.com/english',
                },
            )

        CourseMaterial.objects.get_or_create(
            track=quran_beginners,
            title='Tajweed rules — noon sakinah',
            defaults={
                'material_type': CourseMaterial.TYPE_LINK,
                'external_url': 'https://example.com/quran-tajweed',
            },
        )

        ClassTrackAssignment.objects.get_or_create(
            class_group=class_group,
            track=foundation,
            defaults={'assigned_by': teacher_user},
        )
        ClassTrackAssignment.objects.get_or_create(
            class_group=class_group,
            track=english_core,
            defaults={'assigned_by': teacher_user},
        )

        materials = CourseMaterial.objects.filter(track=foundation).order_by('sort_order')
        if materials.exists():
            mark_material_progress(
                student_profile,
                materials[0],
                StudentMaterialProgress.STATUS_COMPLETED,
                100,
            )
        if materials.count() > 1:
            mark_material_progress(
                student_profile,
                materials[1],
                StudentMaterialProgress.STATUS_IN_PROGRESS,
                45,
            )


def mark_material_progress(student, material, status, progress_percent):
    prog, _ = StudentMaterialProgress.objects.get_or_create(
        student=student,
        material=material,
    )
    prog.status = status
    prog.progress_percent = progress_percent
    if status == StudentMaterialProgress.STATUS_COMPLETED:
        prog.completed_at = timezone.now()
    prog.save()

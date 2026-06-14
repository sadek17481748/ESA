"""pages/tests.py — web registration, school sign-up, homepage, and demo seed."""
import json

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from pages.forms import DEFAULT_SCHOOL_NAME
from parents.models import ParentProfile
from schools.models import School
from students.models import StudentProfile
from academics.models import ClassGroup

User = get_user_model()


class SchoolAdminTeacherTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')

    def test_school_admin_can_add_teacher(self):
        admin = User.objects.get(username='schooladmin')
        self.client.force_login(admin)
        response = self.client.post(reverse('pages:school_admin_add_teacher'), {
            'username': 'newteacher',
            'email': 't@test.com',
            'first_name': 'Tariq',
            'last_name': 'Ali',
            'subject': 'Maths',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertRedirects(response, reverse('pages:school_admin_teachers'))
        self.assertTrue(User.objects.filter(username='newteacher', role='teacher').exists())

    def test_timetable_save_creates_slots(self):
        admin = User.objects.get(username='schooladmin')
        self.client.force_login(admin)
        from subjects.models import Subject
        from timetable.models import Timetable, TimetableSlot
        school = School.objects.get(name='Al-Noor Academy')
        subject = Subject.objects.filter(school=school).first()
        class_group = ClassGroup.objects.filter(school=school).first()
        self.assertIsNotNone(class_group)
        timetable = Timetable.objects.filter(school=school, class_group=class_group).first()
        if not timetable:
            timetable = Timetable.objects.create(
                school=school,
                name=f'{class_group.name} timetable',
                class_group=class_group,
            )
        payload = json.dumps({
            'timetable_id': timetable.pk,
            'class_group_id': class_group.pk,
            'slots': [{
                'weekday': 0,
                'start_time': '08:30',
                'end_time': '09:15',
                'subject_id': subject.pk,
                'teacher_id': class_group.teacher_id,
            }],
        })
        response = self.client.post(
            reverse('pages:timetable_save'),
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(TimetableSlot.objects.filter(timetable=timetable).count(), 1)

    def test_create_timetable_and_subject(self):
        admin = User.objects.get(username='schooladmin')
        self.client.force_login(admin)
        school = School.objects.get(name='Al-Noor Academy')
        class_group = ClassGroup.objects.filter(school=school).first()
        response = self.client.post(
            reverse('pages:timetable_create'),
            data=json.dumps({
                'name': 'Ramadan schedule',
                'class_group_id': class_group.pk,
                'notes': 'Shortened days',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        from timetable.models import Timetable
        self.assertTrue(Timetable.objects.filter(school=school, name='Ramadan schedule').exists())

        response = self.client.post(
            reverse('pages:subject_create'),
            data=json.dumps({'name': 'Tajweed', 'track': 'hifz', 'code': 'TAJ'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        from subjects.models import Subject
        self.assertTrue(Subject.objects.filter(school=school, name='Tajweed').exists())

    def test_school_admin_can_add_class(self):
        admin = User.objects.get(username='schooladmin')
        self.client.force_login(admin)
        school = School.objects.get(name='Al-Noor Academy')
        response = self.client.post(
            reverse('pages:class_create'),
            data=json.dumps({'name': 'Year 9 Test'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body.get('ok'))
        self.assertTrue(ClassGroup.objects.filter(school=school, name='Year 9 Test').exists())

    def test_teacher_cannot_add_class(self):
        teacher = User.objects.get(username='teacher_demo')
        self.client.force_login(teacher)
        response = self.client.post(
            reverse('pages:class_create'),
            data=json.dumps({'name': 'Blocked Class'}),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', response.json())


class DemoSeedTests(TestCase):
    def test_ensure_platform_seed_creates_demo_logins(self):
        call_command('ensure_platform_seed')
        school = School.objects.get(name=DEFAULT_SCHOOL_NAME)
        admin = User.objects.get(username='schooladmin')
        parent = User.objects.get(username='parent_demo')
        self.assertEqual(admin.role, 'school_admin')
        self.assertEqual(admin.school, school)
        self.assertEqual(parent.role, 'parent')
        self.assertTrue(ParentProfile.objects.filter(user=parent).exists())
        self.assertTrue(admin.check_password('admin1234'))
        self.assertTrue(parent.check_password('demo1234'))
        super_user = User.objects.get(username='super')
        self.assertEqual(super_user.role, 'super_admin')
        self.assertTrue(super_user.check_password('super1234'))

    def test_alnoor_seed_creates_30_students_and_parents(self):
        call_command('seed_alnoor_demo')
        school = School.objects.get(name='Al-Noor Academy')
        self.assertEqual(StudentProfile.objects.filter(school=school).count(), 30)
        self.assertGreaterEqual(ParentProfile.objects.filter(school=school).count(), 30)
        self.assertTrue(User.objects.filter(username='mr_mohammed').exists())
        self.assertTrue(ClassGroup.objects.filter(school=school, name='Year 7').exists())


class SuperAdminDashboardTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        self.super_user = User.objects.get(username='super')
        self.parent = User.objects.get(username='parent_demo')

    def test_super_admin_dashboard_loads(self):
        self.client.force_login(self.super_user)
        response = self.client.get(reverse('pages:dashboard_super_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Platform overview')
        self.assertContains(response, 'Al-Noor Academy')
        self.assertContains(response, 'Subscriptions')
        self.assertContains(response, 'Platform activity')

    def test_parent_cannot_access_super_admin_dashboard(self):
        self.client.force_login(self.parent)
        response = self.client.get(reverse('pages:dashboard_super_admin'))
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)

    def test_super_login_lands_on_super_admin_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'super',
            'password': 'super1234',
        })
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)
        response = self.client.get(reverse('pages:dashboard'))
        self.assertRedirects(response, reverse('pages:dashboard_super_admin'), fetch_redirect_response=False)


class HomePageTests(TestCase):
    def test_home_shows_marketing_sections_for_guests(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subscription plans for schools')
        self.assertContains(response, 'Students of the week')
        self.assertContains(response, 'Schools of the week')
        self.assertContains(response, 'Register your school')

    def test_home_shows_dashboard_prompt_when_logged_in(self):
        school = School.objects.create(name=DEFAULT_SCHOOL_NAME)
        user = User.objects.create_user(
            username='homeuser', password='x', role='parent', school=school,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Welcome back')
        self.assertNotContains(response, 'Subscription plans for schools')

    def test_security_page_is_public(self):
        response = self.client.get(reverse('pages:security'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Security on ESA')
        self.assertContains(response, 'Multi-tenant isolation')
        self.assertContains(response, 'Stripe Checkout')


class WebAuthTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(
            name=DEFAULT_SCHOOL_NAME,
            contact_email='admin@alnoor.example',
        )

    def test_register_page_shows_school_picker(self):
        response = self.client.get(reverse('pages:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Al-Noor Academy')
        self.assertContains(response, 'Register a school')
        self.assertContains(response, 'Parent')
        self.assertNotContains(response, 'Teacher')

    def test_register_page_without_schools_prompts_school_signup(self):
        School.objects.all().delete()
        response = self.client.get(reverse('pages:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No schools are registered yet')
        self.assertContains(response, reverse('pages:register_school'))

    def test_register_parent_creates_user_and_logs_in(self):
        response = self.client.post(reverse('pages:register'), {
            'school': self.school.pk,
            'username': 'newparent',
            'email': 'p@test.com',
            'first_name': 'Pat',
            'last_name': 'Parent',
            'role': 'parent',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify_email'))
        user = User.objects.get(username='newparent')
        self.assertEqual(user.school, self.school)
        self.assertTrue(ParentProfile.objects.filter(user=user).exists())

    def test_register_student_creates_profile(self):
        from academics.models import ClassGroup
        cg = ClassGroup.objects.create(school=self.school, name='7Z')
        response = self.client.post(reverse('pages:register'), {
            'school': self.school.pk,
            'username': 'student1',
            'email': 's@test.com',
            'first_name': 'Sam',
            'last_name': 'Student',
            'role': 'student',
            'class_group': cg.pk,
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('verify_email'))
        user = User.objects.get(username='student1')
        self.assertEqual(user.role, 'student')
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

    def test_register_school_adds_to_parent_picker(self):
        response = self.client.post(reverse('pages:register_school'), {
            'school_name': 'Green Valley Madrasa',
            'contact_email': 'office@greenvalley.example',
            'first_name': 'Sara',
            'last_name': 'Admin',
            'username': 'gvadmin',
            'email': 'sara@greenvalley.example',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        new_school = School.objects.get(name='Green Valley Madrasa')
        admin = User.objects.get(username='gvadmin')
        self.assertEqual(admin.role, 'school_admin')
        self.assertEqual(admin.school, new_school)

        self.client.logout()
        picker = self.client.get(reverse('pages:register'))
        self.assertContains(picker, 'Green Valley Madrasa')

    def test_register_school_rejects_duplicate_name(self):
        response = self.client.post(reverse('pages:register_school'), {
            'school_name': 'Al-Noor Academy',
            'contact_email': 'x@test.com',
            'first_name': 'A',
            'last_name': 'B',
            'username': 'dupadmin',
            'email': 'x@test.com',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')

    def test_school_admin_can_log_in_after_register_and_logout(self):
        self.client.post(reverse('pages:register_school'), {
            'school_name': 'Sunrise Madrasa',
            'contact_email': 'office@sunrise.example',
            'first_name': 'Admin',
            'last_name': 'User',
            'username': 'sunriseadmin',
            'email': 'admin@sunrise.example',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.client.get(reverse('logout'))
        response = self.client.post(reverse('login'), {
            'username': 'sunriseadmin',
            'password': 'securepass1',
        })
        self.assertRedirects(response, reverse('verify_email'), fetch_redirect_response=False)

    def test_school_admin_subscription_keeps_sidebar_and_school_name(self):
        self.client.post(reverse('pages:register_school'), {
            'school_name': 'Oak Tree Academy',
            'contact_email': 'a@oak.example',
            'first_name': 'A',
            'last_name': 'B',
            'username': 'oakadmin',
            'email': 'a@oak.example',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        User.objects.filter(username='oakadmin').update(email_verified=True)
        response = self.client.get(reverse('pages:subscription'))
        self.assertRedirects(response, reverse('payments:subscription'))
        response = self.client.get(reverse('payments:subscription'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oak Tree Academy')

    def test_login_page_has_no_demo_credentials(self):
        response = self.client.get(reverse('login'))
        self.assertNotContains(response, 'Demo logins')
        self.assertNotContains(response, 'super1234')

    def test_login_redirects_to_dashboard(self):
        User.objects.create_user(
            username='u1', password='securepass1', role='parent', school=self.school,
            email='u1@esa.demo', email_verified=True,
        )
        response = self.client.post(reverse('login'), {
            'username': 'u1', 'password': 'securepass1',
        })
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)

    def test_register_rejects_duplicate_username(self):
        User.objects.create_user(username='taken', password='x', role='parent', school=self.school)
        response = self.client.post(reverse('pages:register'), {
            'school': self.school.pk,
            'username': 'taken', 'email': 'x@test.com', 'first_name': 'A', 'last_name': 'B',
            'role': 'parent',
            'password1': 'securepass1', 'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already taken')

    def test_logout_redirects_to_home(self):
        user = User.objects.create_user(
            username='u3', password='securepass1', role='parent', school=self.school,
            email='u3@esa.demo', email_verified=True,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)


class AttendancePortalTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        self.school = School.objects.get(name='Al-Noor Academy')
        self.admin = User.objects.get(username='schooladmin')
        self.teacher = User.objects.get(username='mr_mohammed')
        self.class_group = ClassGroup.objects.filter(school=self.school).first()

    def test_school_admin_attendance_overview(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('pages:attendance'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'School attendance')
        self.assertContains(response, self.class_group.name)

    def test_teacher_can_save_register(self):
        self.client.force_login(self.teacher)
        student = StudentProfile.objects.filter(school=self.school).first()
        response = self.client.post(
            reverse('pages:attendance') + f'?class={self.class_group.pk}',
            {f'status_{student.pk}': 'present'},
        )
        self.assertEqual(response.status_code, 302)
        from attendance.models import AttendanceSession
        self.assertTrue(
            AttendanceSession.objects.filter(class_group=self.class_group).exists()
        )

    def test_student_registration_enrols_in_class(self):
        response = self.client.post(reverse('pages:register'), {
            'school': self.school.pk,
            'role': 'student',
            'class_group': self.class_group.pk,
            'first_name': 'New',
            'last_name': 'Student',
            'username': 'new_student_test',
            'email': 'new@test.com',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        from academics.models import ClassEnrollment
        profile = StudentProfile.objects.get(user__username='new_student_test')
        self.assertTrue(
            ClassEnrollment.objects.filter(student=profile, class_group=self.class_group).exists()
        )


class TeacherTimetablePortalTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        from datetime import time

        from subjects.models import Subject
        from teachers.models import TeacherProfile
        from timetable.models import Timetable, TimetableSlot

        self.school = School.objects.get(name='Al-Noor Academy')
        self.teacher_user = User.objects.get(username='mr_mohammed')
        self.teacher_profile = TeacherProfile.objects.get(user=self.teacher_user)
        self.class_group = ClassGroup.objects.filter(school=self.school).first()
        self.subject = Subject.objects.filter(school=self.school, name='Maths').first()
        if not self.subject:
            self.subject = Subject.objects.create(school=self.school, name='Maths', code='MAT')
        self.timetable = Timetable.objects.create(
            school=self.school,
            name='Teacher portal test',
            class_group=self.class_group,
        )
        TimetableSlot.objects.create(
            school=self.school,
            timetable=self.timetable,
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher_profile,
            weekday=0,
            start_time=time(8, 30),
            end_time=time(9, 15),
        )

    def test_teacher_dashboard_shows_assigned_lesson(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('pages:dashboard_teacher'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maths')
        self.assertContains(response, self.class_group.name)
        self.assertContains(response, 'Take register')

    def test_teacher_timetable_page_read_only(self):
        self.client.force_login(self.teacher_user)
        response = self.client.get(reverse('pages:timetable'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My timetable')
        self.assertNotContains(response, 'Save timetable')

    def test_break_subject_always_available(self):
        from subjects.models import Subject
        from pages.timetable_service import ensure_school_subjects, list_school_subjects

        ensure_school_subjects(self.school)
        names = [s.name for s in list_school_subjects(self.school)]
        self.assertIn('Break', names)
        self.assertEqual(names[0], 'Break')

    def test_full_school_seed_creates_y7a_student(self):
        from django.core.management import call_command
        from students.models import StudentProfile

        call_command('seed_alnoor_full_school')
        school = School.objects.get(name='Al-Noor Academy')
        self.assertTrue(
            StudentProfile.objects.filter(school=school, admission_number='Y7A-001').exists()
        )
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='msadekhussain@outlook.com', role='parent').exists())
        self.assertTrue(User.objects.filter(username='msadekhussain2001@gmail.com', role='teacher').exists())

    def test_teacher_register_link_from_timetable_slot(self):
        self.client.force_login(self.teacher_user)
        url = (
            reverse('pages:attendance')
            + f'?class={self.class_group.pk}&subject=Maths'
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maths')
        self.assertContains(response, self.class_group.name)

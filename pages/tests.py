"""pages/tests.py — web registration, school sign-up, homepage, and demo seed."""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from pages.forms import DEFAULT_SCHOOL_NAME
from parents.models import ParentProfile
from schools.models import School
from students.models import StudentProfile

User = get_user_model()


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
        user = User.objects.get(username='newparent')
        self.assertEqual(user.school, self.school)
        self.assertTrue(ParentProfile.objects.filter(user=user).exists())

    def test_register_student_creates_profile(self):
        response = self.client.post(reverse('pages:register'), {
            'school': self.school.pk,
            'username': 'student1',
            'email': 's@test.com',
            'first_name': 'Sam',
            'last_name': 'Student',
            'role': 'student',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
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
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)

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
        response = self.client.get(reverse('pages:subscription'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Oak Tree Academy')
        self.assertContains(response, 'Subscription')
        self.assertContains(response, 'Timetable')

    def test_login_page_has_no_demo_credentials(self):
        response = self.client.get(reverse('login'))
        self.assertNotContains(response, 'Demo logins')
        self.assertNotContains(response, 'super1234')

    def test_login_redirects_to_dashboard(self):
        User.objects.create_user(
            username='u1', password='securepass1', role='parent', school=self.school,
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
        )
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)

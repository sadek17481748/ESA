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


class HomePageTests(TestCase):
    def test_home_shows_marketing_sections_for_guests(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subscription plans for schools')
        self.assertContains(response, 'Compare plans side by side')
        self.assertContains(response, 'Hifz tracking &amp; sign-off')
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

    def test_login_page_shows_demo_credentials(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'schooladmin')
        self.assertContains(response, 'parent_demo')

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

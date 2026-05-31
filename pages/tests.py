"""pages/tests.py — web registration and login redirect."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from parents.models import ParentProfile
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()


class WebAuthTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Existing School', contact_email='a@test.com')

    def test_register_page_loads(self):
        response = self.client.get(reverse('pages:register'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Super Admin')
        self.assertContains(response, 'School Admin')
        self.assertContains(response, 'Teacher')

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('pages:register'), {
            'username': 'newparent',
            'email': 'p@test.com',
            'first_name': 'Pat',
            'last_name': 'Parent',
            'role': 'parent',
            'school_name': 'New Academy',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='newparent')
        self.assertEqual(user.school.name, 'New Academy')
        self.assertTrue(ParentProfile.objects.filter(user=user).exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_register_school_admin_creates_school(self):
        response = self.client.post(reverse('pages:register'), {
            'username': 'admin1',
            'email': 'admin@test.com',
            'first_name': 'Ada',
            'last_name': 'Admin',
            'role': 'school_admin',
            'school_name': 'Al-Noor Academy',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='admin1')
        self.assertEqual(user.role, 'school_admin')
        self.assertEqual(user.school.name, 'Al-Noor Academy')
        self.assertTrue(School.objects.filter(name='Al-Noor Academy').exists())

    def test_register_teacher_joins_school_and_logs_in(self):
        response = self.client.post(reverse('pages:register'), {
            'username': 'teacher1',
            'email': 't@test.com',
            'first_name': 'Tariq',
            'last_name': 'Teacher',
            'role': 'teacher',
            'school_name': 'existing school',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='teacher1')
        self.assertEqual(user.role, 'teacher')
        self.assertEqual(user.school_id, self.school.pk)
        self.assertTrue(TeacherProfile.objects.filter(user=user).exists())

    def test_login_teacher_redirects_to_dashboard(self):
        user = User.objects.create_user(
            username='tlogin', password='securepass1', role='teacher', school=self.school,
        )
        TeacherProfile.objects.create(user=user, school=self.school)
        response = self.client.post(reverse('login'), {
            'username': 'tlogin', 'password': 'securepass1',
        })
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)

    def test_login_school_admin_redirects_to_dashboard(self):
        user = User.objects.create_user(
            username='alogin', password='securepass1', role='school_admin', school=self.school,
        )
        response = self.client.post(reverse('login'), {
            'username': 'alogin', 'password': 'securepass1',
        })
        self.assertRedirects(response, reverse('pages:dashboard'), fetch_redirect_response=False)

    def test_register_joins_existing_school_by_name(self):
        response = self.client.post(reverse('pages:register'), {
            'username': 'student1',
            'email': 's@test.com',
            'first_name': 'Sam',
            'last_name': 'Student',
            'role': 'student',
            'school_name': 'existing school',
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='student1')
        self.assertEqual(user.school_id, self.school.pk)
        self.assertTrue(StudentProfile.objects.filter(user=user).exists())

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
            'username': 'taken', 'email': 'x@test.com', 'first_name': 'A', 'last_name': 'B',
            'role': 'parent', 'school_name': 'Another School',
            'password1': 'securepass1', 'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already taken')

    def test_home_shows_dashboard_link_when_logged_in(self):
        user = User.objects.create_user(
            username='u2', password='securepass1', role='parent', school=self.school,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Dashboard')

    def test_logout_redirects_to_home(self):
        user = User.objects.create_user(
            username='u3', password='securepass1', role='parent', school=self.school,
        )
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)
        self.client.get(reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

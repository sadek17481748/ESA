"""pages/tests.py — web registration and login redirect."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from schools.models import School

User = get_user_model()


class WebAuthTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School', contact_email='a@test.com')

    def test_register_page_loads(self):
        response = self.client.get(reverse('pages:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(reverse('pages:register'), {
            'username': 'newparent',
            'email': 'p@test.com',
            'first_name': 'Pat',
            'last_name': 'Parent',
            'role': 'parent',
            'school': self.school.pk,
            'password1': 'securepass1',
            'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newparent').exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), User.objects.get(username='newparent').pk)

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
            'role': 'parent', 'school': self.school.pk,
            'password1': 'securepass1', 'password2': 'securepass1',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already taken')

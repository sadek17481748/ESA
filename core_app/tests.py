"""core_app/tests.py — homepage leaderboards and platform email."""
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from core_app.email_service import send_platform_email
from schools.models import School
from students.models import StudentProfile


class HomeLeaderboardTests(TestCase):
    def test_homepage_shows_leaderboard_sections(self):
        School.objects.create(name='Test School', contact_email='a@test.com')
        StudentProfile.objects.create(
            school=School.objects.get(name='Test School'),
            first_name='Ali',
            last_name='Khan',
            year_group='Year 7',
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Students of the week')
        self.assertContains(response, 'Schools of the week')

    def test_logged_in_home_skips_leaderboards(self):
        response = self.client.get(reverse('home'))
        # guest sees leaderboards
        self.assertContains(response, 'Students of the week')


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    EMAIL_HOST_USER='test@gmail.com',
    EMAIL_HOST_PASSWORD='app-password',
    ESA_PLATFORM_EMAIL='educationandschoolapplications@gmail.com',
    DEFAULT_FROM_EMAIL='ESA Platform <test@gmail.com>',
)
class PlatformEmailTests(TestCase):
    def test_send_platform_email_delivers_to_inbox(self):
        send_platform_email('Test subject', 'Test body', reply_to='parent@example.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['educationandschoolapplications@gmail.com'])
        self.assertEqual(mail.outbox[0].reply_to, ['parent@example.com'])

"""core_app/tests.py — homepage leaderboards."""
from django.test import TestCase
from django.urls import reverse

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

"""Hifz sign-off tests."""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from hifz.models import HifzJuzSignOff
from messaging.models import SchoolConversation, SchoolMessage
from parents.models import ParentProfile, StudentParentLink
from schools.models import School
from students.models import StudentProfile

User = get_user_model()


class HifzSignOffTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        self.school = School.objects.get(name='Al-Noor Academy')
        self.teacher = User.objects.get(username='teacher_demo')
        self.student = StudentProfile.objects.filter(school=self.school, is_active=True).first()
        self.parent_user = User.objects.filter(role='parent', school=self.school).first()
        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=self.parent_user,
            defaults={'school': self.school},
        )
        StudentParentLink.objects.get_or_create(
            parent=parent_profile,
            student=self.student,
            defaults={'relationship': 'guardian'},
        )

    def test_teacher_sign_off_sends_parent_message(self):
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('pages:hifz'), {
            'student': self.student.pk,
            'juz_number': '3',
        })
        self.assertRedirects(response, reverse('pages:hifz'))
        self.assertTrue(
            HifzJuzSignOff.objects.filter(student=self.student, juz_number=3).exists(),
        )
        conv = SchoolConversation.objects.filter(
            created_by=self.teacher,
            recipient_user=self.parent_user,
            subject='Hifz — Juz 3 passed',
        ).first()
        self.assertIsNotNone(conv)
        msg = SchoolMessage.objects.filter(conversation=conv).first()
        self.assertIn('Congratulations', msg.body)
        self.assertIn('Juz 3', msg.body)

    def test_duplicate_sign_off_rejected(self):
        self.client.force_login(self.teacher)
        self.client.post(reverse('pages:hifz'), {
            'student': self.student.pk,
            'juz_number': '5',
        })
        response = self.client.post(reverse('pages:hifz'), {
            'student': self.student.pk,
            'juz_number': '5',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            HifzJuzSignOff.objects.filter(student=self.student, juz_number=5).count(),
            1,
        )

    def test_parent_sees_sign_offs(self):
        self.client.force_login(self.teacher)
        self.client.post(reverse('pages:hifz'), {
            'student': self.student.pk,
            'juz_number': '1',
        })
        self.client.force_login(self.parent_user)
        response = self.client.get(reverse('pages:hifz'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juz 1')
        self.assertContains(response, self.student.full_name)

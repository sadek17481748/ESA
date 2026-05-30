"""Verify Al-Noor demo examples seed."""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from lms.models import StudentMaterialProgress
from messaging.models import SchoolConversation, SupportCase, TeacherReport
from students.models import StudentProfile

User = get_user_model()


class AlNoorExamplesSeedTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')

    def test_test_accounts_exist_with_examples(self):
        parent = User.objects.get(username='test_parent')
        student = User.objects.get(username='test_student')
        self.assertEqual(parent.school.name, 'Al-Noor Academy')
        profile = StudentProfile.objects.get(user=student)
        self.assertTrue(SupportCase.objects.filter(opened_by=parent).exists())
        self.assertTrue(SchoolConversation.objects.filter(created_by=parent).exists())
        self.assertTrue(TeacherReport.objects.filter(student=profile).exists())
        self.assertTrue(StudentMaterialProgress.objects.filter(student=profile).exists())

    def test_test_parent_can_open_inbox(self):
        self.client.force_login(User.objects.get(username='test_parent'))
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ESA-00001')

    def test_test_student_sees_lms_progress(self):
        self.client.force_login(User.objects.get(username='test_student'))
        response = self.client.get(reverse('pages:worksheets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My learning')

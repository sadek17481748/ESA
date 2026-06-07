"""
subjects/tests.py
Hifz / Alimiyah subjects must have a lead teacher.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from schools.models import School
from teachers.models import TeacherProfile

User = get_user_model()


class SubjectValidationTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='S')
        self.admin = User.objects.create_user(
            username='admin', password='x', role='school_admin', school=self.school,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

    def test_hifz_without_lead_teacher_rejected(self):
        response = self.client.post(
            '/api/subjects/',
            {'name': 'Hifz Level 1', 'track': 'hifz'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)

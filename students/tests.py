"""
students/tests.py
Checks tenant scoping on GET /api/students/ — teacher only sees own school.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from schools.models import School
from students.models import StudentProfile

User = get_user_model()


class StudentTenantTests(TestCase):
    def setUp(self):
        self.school_a = School.objects.create(name='A')
        self.school_b = School.objects.create(name='B')
        self.teacher = User.objects.create_user(
            username='t1', password='x', role='teacher', school=self.school_a,
        )
        StudentProfile.objects.create(
            school=self.school_a, first_name='Ali', last_name='One', admission_number='1',
        )
        StudentProfile.objects.create(
            school=self.school_b, first_name='Sara', last_name='Two', admission_number='2',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.teacher)

    def test_teacher_only_sees_own_school_students(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Ali')

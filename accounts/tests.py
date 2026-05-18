from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from schools.models import School

User = get_user_model()


class TenantApiTests(TestCase):
    def setUp(self):
        self.school_a = School.objects.create(name='School A')
        self.school_b = School.objects.create(name='School B')
        self.admin_a = User.objects.create_user(
            username='admin_a', password='pass', role='school_admin', school=self.school_a,
        )
        self.admin_b = User.objects.create_user(
            username='admin_b', password='pass', role='school_admin', school=self.school_b,
        )
        self.client = APIClient()

    def test_school_admin_only_sees_own_school(self):
        self.client.force_authenticate(self.admin_a)
        response = self.client.get('/api/schools/')
        self.assertEqual(response.status_code, 200)
        ids = [row['id'] for row in response.data]
        self.assertEqual(ids, [self.school_a.id])

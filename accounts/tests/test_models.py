from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import UserRole

User = get_user_model()


class UserModelTests(TestCase):
    def test_default_role_is_student(self):
        user = User.objects.create_user(username="u1", password="test-pass-123")
        self.assertEqual(user.role, UserRole.STUDENT)

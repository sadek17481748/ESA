from django.contrib.auth import get_user_model
from django.test import TestCase

from schools.models import School
from payments.models import FeeItem

User = get_user_model()


class FeeItemModelTests(TestCase):
    def test_amount_display_formats_pence(self):
        school = School.objects.create(name='Test School')
        parent = User.objects.create_user(username='p1', password='x', role='parent', school=school)
        fee = FeeItem.objects.create(
            school=school,
            parent=parent,
            child_name='Test Child',
            title='Tuition',
            amount_pence=25000,
            due_date='2026-06-01',
        )
        self.assertEqual(fee.amount_display, '£250.00')

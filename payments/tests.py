"""
payments/tests.py
Fee models and school admin fee management.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from parents.models import ParentProfile, StudentParentLink
from schools.models import School
from payments.models import FeeItem
from students.models import StudentProfile

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


class SchoolAdminFeesTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Fee Test School')
        self.admin = User.objects.create_user(
            username='fee_admin', password='pass', role='school_admin', school=self.school,
        )
        self.parent = User.objects.create_user(
            username='fee_parent', password='pass', role='parent', school=self.school,
        )
        self.parent_profile = ParentProfile.objects.create(school=self.school, user=self.parent)
        self.student = StudentProfile.objects.create(
            school=self.school,
            user=User.objects.create_user(
                username='fee_student', password='pass', role='student', school=self.school,
            ),
            first_name='Aisha',
            last_name='Khan',
            year_group='Year 7',
            admission_number='FT001',
        )
        StudentParentLink.objects.create(
            parent=self.parent_profile, student=self.student, relationship='guardian',
        )
        self.client = Client()

    def test_school_admin_sees_fee_manager(self):
        self.client.login(username='fee_admin', password='pass')
        response = self.client.get(reverse('payments:school_fees'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Aisha Khan')
        self.assertContains(response, 'Set a fee')

    def test_parent_cannot_access_school_fees(self):
        self.client.login(username='fee_parent', password='pass')
        response = self.client.get(reverse('payments:school_fees'))
        self.assertEqual(response.status_code, 302)

    def test_school_admin_redirected_from_parent_fee_list(self):
        self.client.login(username='fee_admin', password='pass')
        response = self.client.get(reverse('payments:fee_list'))
        self.assertRedirects(response, reverse('payments:school_fees'))

    def test_create_fee_for_all_students(self):
        self.client.login(username='fee_admin', password='pass')
        response = self.client.post(reverse('payments:school_fees'), {
            'action': 'create',
            'title': 'Spring term',
            'amount_pounds': '120.50',
            'due_date': (date.today() + timedelta(days=21)).isoformat(),
            'student': '',
        })
        self.assertRedirects(response, reverse('payments:school_fees'))
        fee = FeeItem.objects.get(parent=self.parent, title='Spring term')
        self.assertEqual(fee.amount_pence, 12050)
        self.assertEqual(fee.child_name, 'Aisha Khan')

    def test_mark_fee_paid(self):
        fee = FeeItem.objects.create(
            school=self.school,
            parent=self.parent,
            child_name='Aisha Khan',
            title='Trip',
            amount_pence=3500,
            due_date=date.today(),
            status=FeeItem.STATUS_OUTSTANDING,
        )
        self.client.login(username='fee_admin', password='pass')
        response = self.client.post(reverse('payments:school_fees'), {
            'action': 'mark_paid',
            'fee_id': fee.pk,
        })
        self.assertRedirects(response, reverse('payments:school_fees'))
        fee.refresh_from_db()
        self.assertEqual(fee.status, FeeItem.STATUS_PAID)

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
            email='admin@feetest.example', email_verified=True,
        )
        self.parent = User.objects.create_user(
            username='fee_parent', password='pass', role='parent', school=self.school,
            email='parent@feetest.example', email_verified=True,
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


class ParentPaymentPortalTests(TestCase):
    """Manual rows 12–13, 16–17 — parent fees, redirect, cancel, idempotent success."""

    def setUp(self):
        self.school = School.objects.create(name='Pay Portal School')
        self.parent = User.objects.create_user(
            username='pay_parent', password='pass', role='parent', school=self.school,
            email='pay@feetest.example', email_verified=True,
        )
        ParentProfile.objects.create(school=self.school, user=self.parent)
        other_parent = User.objects.create_user(
            username='other_parent', password='pass', role='parent', school=self.school,
        )
        self.own_fee = FeeItem.objects.create(
            school=self.school,
            parent=self.parent,
            child_name='Child A',
            title='Term fee',
            amount_pence=5000,
            due_date=date.today(),
        )
        FeeItem.objects.create(
            school=self.school,
            parent=other_parent,
            child_name='Child B',
            title='Other fee',
            amount_pence=3000,
            due_date=date.today(),
        )
        self.client = Client()

    def test_row_12_parent_sees_own_fees_only(self):
        self.client.login(username='pay_parent', password='pass')
        response = self.client.get(reverse('payments:fee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Term fee')
        self.assertNotContains(response, 'Other fee')

    def test_row_13_unauthenticated_payments_redirect(self):
        response = self.client.get(reverse('payments:fee_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_row_16_stripe_cancel_page(self):
        self.client.login(username='pay_parent', password='pass')
        response = self.client.get(reverse('payments:cancel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cancelled')

    def test_row_17_no_duplicate_payment_on_refresh(self):
        from unittest.mock import patch
        from payments.models import Payment

        class FakeStripeSession:
            id = 'cs_test_dup_1'
            payment_status = 'paid'
            amount_total = 5000
            currency = 'gbp'
            payment_intent = 'pi_test'
            metadata = None

            def __init__(self, fee_id):
                self.metadata = {'fee_item_id': str(fee_id), 'payment_type': 'fee'}

            def get(self, key, default=None):
                return getattr(self, key, default)

        self.client.login(username='pay_parent', password='pass')
        session = FakeStripeSession(self.own_fee.pk)
        with patch('payments.views.retrieve_checkout_session', return_value=session):
            url = reverse('payments:success') + '?session_id=cs_test_dup_1'
            self.client.get(url)
            self.client.get(url)
        self.assertEqual(Payment.objects.filter(stripe_session_id='cs_test_dup_1').count(), 1)


class SubscriptionSyncTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Sub School', subscription_tier=School.TIER_FREE)
        self.admin = User.objects.create_user(
            username='sub_admin', password='pass', role='school_admin', school=self.school,
        )

    def test_apply_subscription_updates_tier(self):
        from payments.subscription_sync import apply_subscription_from_session

        session = {
            'id': 'cs_test_sub_1',
            'amount_total': 4900,
            'payment_intent': 'pi_test',
            'metadata': {
                'payment_type': 'subscription',
                'school_id': str(self.school.pk),
                'tier': 'standard',
                'admin_user_id': str(self.admin.pk),
            },
        }
        payment = apply_subscription_from_session(session)
        self.assertIsNotNone(payment)
        self.school.refresh_from_db()
        self.assertEqual(self.school.subscription_tier, School.TIER_STANDARD)

    def test_apply_subscription_idempotent(self):
        from payments.subscription_sync import apply_subscription_from_session

        session = {
            'id': 'cs_test_sub_2',
            'amount_total': 9900,
            'payment_intent': 'pi_test2',
            'metadata': {
                'payment_type': 'subscription',
                'school_id': str(self.school.pk),
                'tier': 'premium',
                'admin_user_id': str(self.admin.pk),
            },
        }
        apply_subscription_from_session(session)
        apply_subscription_from_session(session)
        from payments.models import SubscriptionPayment
        self.assertEqual(SubscriptionPayment.objects.filter(stripe_session_id='cs_test_sub_2').count(), 1)
        self.school.refresh_from_db()
        self.assertEqual(self.school.subscription_tier, School.TIER_PREMIUM)

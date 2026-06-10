"""accounts/tests_auth.py — email verification and password reset."""
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import EmailVerificationCode
from accounts.verification import (
    create_and_send_verification_code,
    is_reserved_demo_email,
    user_needs_email_verification,
    verify_email_code,
)
from parents.models import ParentProfile, StudentParentLink
from schools.models import School
from students.link_service import get_or_create_active_code, link_parent_to_student
from students.models import StudentProfile

User = get_user_model()


class EmailVerificationTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School')

    def test_demo_email_exempt(self):
        user = User.objects.create_user(
            username='parent_demo', email='parent@esa.demo', password='x',
            role='parent', school=self.school, email_verified=False,
        )
        self.assertFalse(user_needs_email_verification(user))

    def test_real_email_requires_verification(self):
        user = User.objects.create_user(
            username='realparent', email='parent@realmail.com', password='x',
            role='parent', school=self.school,
        )
        self.assertTrue(user_needs_email_verification(user))

    def test_reserved_demo_email_blocked_on_register(self):
        self.assertTrue(is_reserved_demo_email('x@esa.demo'))

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_verification_code_flow(self):
        user = User.objects.create_user(
            username='verifyme', email='verify@test.com', password='x',
            role='parent', school=self.school,
        )
        ParentProfile.objects.create(user=user, school=self.school)
        create_and_send_verification_code(user)
        self.assertEqual(len(mail.outbox), 1)
        code = EmailVerificationCode.objects.filter(user=user).latest('created_at').code
        ok, _ = verify_email_code(user, code)
        self.assertTrue(ok)
        user.refresh_from_db()
        self.assertTrue(user.email_verified)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School')
        self.user = User.objects.create_user(
            username='resetuser', email='reset@test.com', password='oldpass1234',
            role='parent', school=self.school, email_verified=True,
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_sends_email(self):
        response = self.client.post(reverse('password_reset'), {'email': 'reset@test.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('[ESA] Password reset', mail.outbox[0].subject)


class StudentLinkCodeTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Link School')
        self.student = StudentProfile.objects.create(
            school=self.school, first_name='Ali', last_name='Hassan', admission_number='L1',
        )
        self.parent_user = User.objects.create_user(
            username='linkparent', email='linkparent@test.com', password='x',
            role='parent', school=self.school, email_verified=True,
        )
        ParentProfile.objects.create(user=self.parent_user, school=self.school)

    def test_parent_links_with_code(self):
        code_row = get_or_create_active_code(student=self.student)
        _, created, student = link_parent_to_student(
            parent_user=self.parent_user, code=code_row.code,
        )
        self.assertTrue(created)
        self.assertEqual(student, self.student)
        self.assertTrue(StudentParentLink.objects.filter(student=self.student).exists())

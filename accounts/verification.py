"""
accounts/verification.py
Email verification codes and demo-account bypass rules.
"""
import random
import string
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from core_app.email_service import send_user_email

from .models import EmailVerificationCode

# Demo / seed accounts skip verification (see README test credentials)
EXEMPT_EMAIL_DOMAINS = ('esa.demo', 'alnoor.example')
EXEMPT_USERNAMES = frozenset({
    'super', 'schooladmin', 'parent_demo', 'teacher_demo', 'student_demo',
    'test_parent', 'test_student',
})


def email_domain(email):
    email = (email or '').strip().lower()
    if '@' not in email:
        return ''
    return email.rsplit('@', 1)[-1]


def is_demo_email(email):
    domain = email_domain(email)
    return any(domain == d or domain.endswith('.' + d) for d in EXEMPT_EMAIL_DOMAINS)


def is_reserved_demo_email(email):
    """Block new registrations using internal demo domains."""
    return is_demo_email(email)


def user_needs_email_verification(user):
    if not user or not user.is_authenticated:
        return False
    if getattr(user, 'email_verified', False):
        return False
    if user.username.lower() in EXEMPT_USERNAMES:
        return False
    if is_demo_email(user.email):
        return False
    return True


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


def create_and_send_verification_code(user, *, request=None):
    """Invalidate old codes, create a new 6-digit code, email it to the user."""
    EmailVerificationCode.objects.filter(user=user, is_used=False).update(is_used=True)
    code = generate_verification_code()
    expires = timezone.now() + timedelta(minutes=15)
    EmailVerificationCode.objects.create(user=user, code=code, expires_at=expires)

    body = (
        f'Hello {user.first_name or user.username},\n\n'
        f'Your ESA verification code is: {code}\n\n'
        f'This code expires in 15 minutes. If you did not create an account, ignore this email.\n'
    )
    sent = send_user_email('[ESA] Verify your email', body, [user.email])

    # Dev / console backend — code still works via DB; optional debug hint
    if not sent and getattr(settings, 'DEBUG', False):
        return code, False
    return code, sent


def verify_email_code(user, code):
    code = (code or '').strip()
    if not code:
        return False, 'Enter the 6-digit code from your email.'
    row = (
        EmailVerificationCode.objects.filter(
            user=user, code=code, is_used=False, expires_at__gte=timezone.now(),
        )
        .order_by('-created_at')
        .first()
    )
    if not row:
        return False, 'Invalid or expired code. Request a new one.'
    row.is_used = True
    row.save(update_fields=['is_used'])
    user.email_verified = True
    user.save(update_fields=['email_verified'])
    return True, 'Email verified — welcome to ESA.'

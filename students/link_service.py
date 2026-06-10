"""
students/link_service.py
School-issued codes so parents can link to a student profile.
"""
import secrets
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from parents.models import ParentProfile, StudentParentLink

from .models import StudentLinkCode, StudentProfile


def generate_link_code():
    return secrets.token_hex(4).upper()


def get_or_create_active_code(*, student, created_by=None):
    existing = StudentLinkCode.objects.filter(
        student=student, is_active=True, expires_at__gte=timezone.now(),
    ).order_by('-created_at').first()
    if existing:
        return existing
    StudentLinkCode.objects.filter(student=student, is_active=True).update(is_active=False)
    expires = timezone.now() + timedelta(days=90)
    return StudentLinkCode.objects.create(
        student=student,
        school=student.school,
        code=generate_link_code(),
        created_by=created_by,
        expires_at=expires,
    )


def regenerate_link_code(*, student, created_by=None):
    StudentLinkCode.objects.filter(student=student, is_active=True).update(is_active=False)
    expires = timezone.now() + timedelta(days=90)
    return StudentLinkCode.objects.create(
        student=student,
        school=student.school,
        code=generate_link_code(),
        created_by=created_by,
        expires_at=expires,
    )


def resolve_link_code(code):
    code = (code or '').strip().upper()
    if not code:
        return None
    return StudentLinkCode.objects.filter(
        code__iexact=code,
        is_active=True,
        expires_at__gte=timezone.now(),
    ).select_related('student', 'school').first()


def link_parent_to_student(*, parent_user, code, relationship='guardian'):
    if parent_user.role != 'parent':
        raise PermissionError('Only parent accounts can link to a student.')
    link_row = resolve_link_code(code)
    if not link_row:
        raise ValueError('Invalid or expired link code.')
    if parent_user.school_id != link_row.school_id:
        raise ValueError('This code belongs to a different school than your account.')

    parent_profile, _ = ParentProfile.objects.get_or_create(
        user=parent_user,
        defaults={'school': link_row.school},
    )
    if parent_profile.school_id != link_row.school_id:
        raise ValueError('Your parent profile is registered at another school.')

    obj, created = StudentParentLink.objects.get_or_create(
        parent=parent_profile,
        student=link_row.student,
        defaults={'relationship': relationship},
    )
    return obj, created, link_row.student


def build_parent_link_url(request, code):
    path = reverse('pages:parent_link_child') + f'?code={code}'
    return request.build_absolute_uri(path)

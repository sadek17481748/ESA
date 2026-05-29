"""messaging/services.py — case numbers and conversation access."""
from django.db.models import Q

from .models import SchoolConversation, SupportCase


def generate_case_number():
    prefix = 'ESA'
    last = SupportCase.objects.order_by('-pk').first()
    seq = (last.pk + 1) if last else 1
    return f'{prefix}-{seq:05d}'


def user_can_view_conversation(user, conversation):
    if conversation.created_by_id == user.pk:
        return True
    if conversation.recipient_user_id == user.pk:
        return True
    if conversation.recipient_type == SchoolConversation.RECIPIENT_SCHOOL:
        if user.role == 'school_admin' and user.school_id == conversation.school_id:
            return True
    if user.role == 'school_admin' and user.school_id == conversation.school_id:
        if conversation.created_by.role in ('parent', 'teacher'):
            return True
    return False


def conversations_for_user(user):
    school = user.school
    if not school and user.role != 'super_admin':
        return SchoolConversation.objects.none()

    if user.role == 'school_admin':
        return SchoolConversation.objects.filter(school=school).select_related(
            'created_by', 'recipient_user',
        )

    return SchoolConversation.objects.filter(
        Q(created_by=user) | Q(recipient_user=user),
        school=school,
    ).select_related('created_by', 'recipient_user')


def support_cases_for_user(user):
    if user.role == 'super_admin':
        return SupportCase.objects.select_related('opened_by').all()
    return SupportCase.objects.filter(opened_by=user)

"""payments/overdue.py — mark overdue fees and notify parents."""
from datetime import date

from django.utils import timezone

from core_app.email_service import send_user_email
from notifications.services import notify_user

from .models import FeeItem


def mark_overdue_fees(*, school=None, today=None):
    """Flip outstanding fees past due_date to overdue; return newly marked rows."""
    today = today or date.today()
    qs = FeeItem.objects.filter(
        status=FeeItem.STATUS_OUTSTANDING,
        due_date__lt=today,
    ).select_related('parent', 'school')
    if school:
        qs = qs.filter(school=school)
    updated = []
    for fee in qs:
        fee.status = FeeItem.STATUS_OVERDUE
        fee.save(update_fields=['status'])
        updated.append(fee)
    return updated


def notify_overdue_fee(fee):
    parent = fee.parent
    if not parent:
        return
    title = f'Fee overdue — {fee.title}'
    message = (
        f'{fee.child_name}: {fee.title} was due {fee.due_date}. '
        f'Amount £{fee.amount_pence / 100:.2f}. Please pay via the parent portal.'
    )
    notify_user(
        user=parent,
        school=fee.school,
        notification_type='general',
        title=title,
        message=message,
        link_path='/payments/',
    )
    if parent.email:
        send_user_email(
            f'[ESA] {title}',
            f'{message}\n\nLog in: /payments/\n',
            [parent.email],
        )


def process_overdue_reminders(*, school=None):
    fees = mark_overdue_fees(school=school)
    for fee in fees:
        notify_overdue_fee(fee)
    return fees

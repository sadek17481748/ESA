"""Apply subscription tier from Stripe checkout session — shared by success page and webhook."""
import uuid

from django.contrib.auth import get_user_model
from django.utils import timezone

from schools.models import School

from .models import SubscriptionPayment
from .subscription_plans import plan_for_tier

User = get_user_model()


def valid_subscription_tier(tier):
    plan = plan_for_tier(tier)
    return plan['tier'] if plan else None


def apply_subscription_from_session(session):
    """
    Idempotent subscription completion from Stripe checkout session dict/object.
    Returns SubscriptionPayment or None.
    """
    session_id = session.get('id')
    if not session_id:
        return None

    existing = SubscriptionPayment.objects.filter(stripe_session_id=session_id).first()
    if existing:
        _ensure_school_tier(existing.school, existing.tier)
        return existing

    metadata = session.get('metadata') or {}
    school_id = metadata.get('school_id')
    tier = metadata.get('tier')
    tier = valid_subscription_tier(tier)
    if not school_id or not tier:
        return None

    payment_type = metadata.get('payment_type', '')
    if payment_type and payment_type != 'subscription':
        return None

    try:
        school = School.objects.get(pk=school_id)
    except School.DoesNotExist:
        return None

    admin_id = metadata.get('admin_user_id')
    admin = User.objects.filter(pk=admin_id).first() if admin_id else None
    if not admin:
        admin = User.objects.filter(school=school, role='school_admin').first()
    if not admin:
        return None

    payment = SubscriptionPayment.objects.create(
        school=school,
        admin=admin,
        tier=tier,
        amount_pence=session.get('amount_total') or 0,
        stripe_session_id=session_id,
        stripe_payment_intent=session.get('payment_intent') or '',
        status=SubscriptionPayment.STATUS_COMPLETE,
        receipt_reference=uuid.uuid4().hex[:12].upper(),
        paid_at=timezone.now(),
    )
    _ensure_school_tier(school, tier)
    from .notifications import notify_platform_subscription_payment
    notify_platform_subscription_payment(payment)
    return payment


def _ensure_school_tier(school, tier):
    tier = valid_subscription_tier(tier)
    if tier and school.subscription_tier != tier:
        school.subscription_tier = tier
        school.save(update_fields=['subscription_tier'])

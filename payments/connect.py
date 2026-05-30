"""
payments/connect.py
Stripe Connect Express onboarding and destination charges to school accounts.
"""
import stripe
from django.conf import settings

from .services import configure_stripe

PLATFORM_FEE_PERCENT = getattr(settings, 'STRIPE_PLATFORM_FEE_PERCENT', 0)


def school_has_connect(school):
    return bool(school and school.stripe_account_id)


def create_connect_onboarding_link(*, school, return_url, refresh_url):
    """Create or reuse a Connect Express account and return onboarding URL."""
    configure_stripe()
    if not school.stripe_account_id:
        account = stripe.Account.create(
            type='express',
            country='GB',
            capabilities={'card_payments': {'requested': True}, 'transfers': {'requested': True}},
            business_type='company',
            metadata={'school_id': str(school.pk), 'school_name': school.name},
        )
        school.stripe_account_id = account.id
        school.save(update_fields=['stripe_account_id'])

    link = stripe.AccountLink.create(
        account=school.stripe_account_id,
        refresh_url=refresh_url,
        return_url=return_url,
        type='account_onboarding',
    )
    return link.url


def connect_status(school):
    """Return charges_enabled flag for dashboard badge."""
    if not school.stripe_account_id:
        return {'connected': False, 'charges_enabled': False, 'details_submitted': False}
    configure_stripe()
    account = stripe.Account.retrieve(school.stripe_account_id)
    return {
        'connected': True,
        'charges_enabled': bool(account.charges_enabled),
        'details_submitted': bool(account.details_submitted),
        'account_id': school.stripe_account_id,
    }


def apply_connect_to_checkout_kwargs(kwargs, *, school, amount_pence):
    """Route fee payment to connected account with optional platform fee."""
    if not school.stripe_account_id:
        return kwargs
    fee_amount = 0
    if PLATFORM_FEE_PERCENT:
        fee_amount = int(amount_pence * PLATFORM_FEE_PERCENT / 100)
    kwargs['payment_intent_data'] = {
        'transfer_data': {'destination': school.stripe_account_id},
    }
    if fee_amount > 0:
        kwargs['payment_intent_data']['application_fee_amount'] = fee_amount
    return kwargs

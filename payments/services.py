"""
payments/services.py
Stripe Checkout session helpers — keys from settings / .env.
"""
import stripe
from django.conf import settings


def stripe_is_configured():
    return bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_PUBLISHABLE_KEY)


def configure_stripe():
    """Set global API key before any stripe.* call."""
    if not settings.STRIPE_SECRET_KEY:
        raise stripe.error.AuthenticationError('Stripe secret key is not configured.')
    stripe.api_key = settings.STRIPE_SECRET_KEY


def create_fee_checkout_session(*, fee_item, success_url, cancel_url, customer_email=None):
    """
    Start a one-off Checkout session for a single FeeItem.
    unit_amount must be in pence for GBP.
    """
    configure_stripe()

    line_items = [{
        'price_data': {
            'currency': 'gbp',
            'unit_amount': fee_item.amount_pence,
            'product_data': {
                'name': fee_item.title,
                'description': f'{fee_item.child_name} — {fee_item.school.name}',
            },
        },
        'quantity': 1,
    }]

    kwargs = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'metadata': {
            'payment_type': 'fee',
            'fee_item_id': str(fee_item.pk),
            'school_id': str(fee_item.school_id),
        },
    }
    if customer_email:
        kwargs['customer_email'] = customer_email

    return stripe.checkout.Session.create(**kwargs)


def create_subscription_checkout_session(
    *,
    school,
    tier,
    plan_name,
    amount_pence,
    success_url,
    cancel_url,
    customer_email=None,
    admin_user_id=None,
):
    """Checkout for school admin upgrading ESA subscription (one-off monthly payment)."""
    configure_stripe()

    line_items = [{
        'price_data': {
            'currency': 'gbp',
            'unit_amount': amount_pence,
            'product_data': {
                'name': f'ESA {plan_name} plan',
                'description': f'Monthly subscription for {school.name}',
            },
        },
        'quantity': 1,
    }]

    kwargs = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': success_url,
        'cancel_url': cancel_url,
        'metadata': {
            'payment_type': 'subscription',
            'school_id': str(school.pk),
            'tier': tier,
            'admin_user_id': str(admin_user_id or ''),
        },
    }
    if customer_email:
        kwargs['customer_email'] = customer_email

    return stripe.checkout.Session.create(**kwargs)


def retrieve_checkout_session(session_id):
    """Pull session from Stripe after redirect (success page)."""
    configure_stripe()
    return stripe.checkout.Session.retrieve(session_id)

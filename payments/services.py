"""
payments/services.py
Stripe Checkout session helpers — keys from settings / .env.
"""
import stripe
from django.conf import settings


def configure_stripe():
    """Set global API key before any stripe.* call."""
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
            'fee_item_id': str(fee_item.pk),
            'school_id': str(fee_item.school_id),
        },
    }
    if customer_email:
        kwargs['customer_email'] = customer_email

    return stripe.checkout.Session.create(**kwargs)


def retrieve_checkout_session(session_id):
    """Pull session from Stripe after redirect (success page)."""
    configure_stripe()
    return stripe.checkout.Session.retrieve(session_id)


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — Stripe needs pence; this charged £2.50 instead of £250
# ---------------------------------------------------------------------------
# def create_fee_checkout_session(*, fee_item, success_url, cancel_url, customer_email=None):
#     line_items = [{
#         'price_data': {
#             'currency': 'gbp',
#             'unit_amount': fee_item.amount_pence // 100,
#             'product_data': {'name': fee_item.title},
#         },
#         'quantity': 1,
#     }]
#     return stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url=success_url,
#         cancel_url=cancel_url,
#     )

# bug: forgot configure_stripe() first — "No API key provided"
# return stripe.checkout.Session.create(...)

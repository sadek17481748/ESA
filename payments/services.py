"""Stripe helpers — checkout sessions for parent school fees."""

import stripe
from django.conf import settings


def configure_stripe():
    stripe.api_key = settings.STRIPE_SECRET_KEY


def create_fee_checkout_session(*, fee_item, success_url, cancel_url, customer_email=None):
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
    configure_stripe()
    return stripe.checkout.Session.retrieve(session_id)


# --- old bug: passed pounds into unit_amount ---
# 'unit_amount': fee_item.amount_pence // 100,

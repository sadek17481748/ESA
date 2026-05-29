"""payments/subscription_plans.py — ESA school subscription tiers for Stripe Checkout."""
from django.conf import settings

PLANS = {
    'standard': {
        'key': 'standard',
        'name': 'Standard',
        'tagline': 'Full teaching tools, parent portals, and Hifz tracking.',
        'amount_pence': settings.SUBSCRIPTION_PRICES['standard'],
        'price_display': f'£{settings.SUBSCRIPTION_PRICES["standard"] // 100}',
        'tier': 'standard',
        'features': [
            'Up to 200 students',
            'Up to 25 staff accounts',
            'Hifz tracking & homework',
            'Parent & student portals',
        ],
    },
    'premium': {
        'key': 'premium',
        'name': 'Premium',
        'tagline': 'Payments, analytics, messaging, and unlimited scale.',
        'amount_pence': settings.SUBSCRIPTION_PRICES['premium'],
        'price_display': f'£{settings.SUBSCRIPTION_PRICES["premium"] // 100}',
        'tier': 'premium',
        'features': [
            'Unlimited students & staff',
            'Stripe fee payments for parents',
            'Analytics dashboard',
            'Staff messaging & behaviour logs',
        ],
    },
}


def plan_for_tier(tier_key):
    return PLANS.get(tier_key)


def plan_amount_display(pence):
    return f'£{pence / 100:.0f}'

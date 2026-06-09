"""Email alerts for fee and subscription payments."""
from core_app.email_service import send_platform_email


def notify_platform_subscription_payment(payment):
    """Email platform inbox when a school upgrades subscription."""
    school = payment.school
    admin = payment.admin
    amount = f'£{payment.amount_pence / 100:.2f}'
    body = (
        f'A school has subscribed on ESA.\n\n'
        f'School: {school.name}\n'
        f'Plan: {payment.tier.title()}\n'
        f'Amount: {amount}\n'
        f'Admin: {admin.get_full_name() or admin.username} ({admin.email or "no email"})\n'
        f'Receipt: {payment.receipt_reference}\n'
        f'Stripe session: {payment.stripe_session_id}\n'
    )
    send_platform_email(
        f'[ESA] New subscription — {school.name} ({payment.tier.title()})',
        body,
        reply_to=admin.email or None,
    )


def notify_platform_fee_payment(payment):
    """Email platform inbox when a parent pays a school fee."""
    fee = payment.fee_item
    parent = payment.parent
    amount = f'£{payment.amount_pence / 100:.2f}'
    body = (
        f'A parent fee payment was completed on ESA.\n\n'
        f'School: {fee.school.name}\n'
        f'Fee: {fee.title}\n'
        f'Child: {fee.child_name}\n'
        f'Amount: {amount}\n'
        f'Parent: {parent.get_full_name() or parent.username} ({parent.email or "no email"})\n'
        f'Receipt: {payment.receipt_reference}\n'
    )
    send_platform_email(
        f'[ESA] Fee paid — {fee.school.name} — {fee.title}',
        body,
        reply_to=parent.email or None,
    )

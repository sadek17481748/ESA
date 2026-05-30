"""payments/receipt.py — printable HTML receipt (save as PDF from browser)."""
from django.utils import timezone


def receipt_context(payment):
    fee = payment.fee_item
    return {
        'payment': payment,
        'fee': fee,
        'school': fee.school,
        'parent': payment.parent,
        'issued_at': payment.paid_at or timezone.now(),
        'amount_display': f'£{payment.amount_pence / 100:.2f}',
    }

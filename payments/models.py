"""
payments/models.py
School fees (FeeItem) and Stripe payment records (Payment).
"""
from django.conf import settings
from django.db import models

from schools.models import School


class FeeItem(models.Model):
    """A fee charged to a parent — tuition, trip, etc."""

    STATUS_OUTSTANDING = 'outstanding'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'
    STATUS_CHOICES = [
        (STATUS_OUTSTANDING, 'Outstanding'),
        (STATUS_PAID, 'Paid'),
        (STATUS_OVERDUE, 'Overdue'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='fee_items')
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fee_items',
        limit_choices_to={'role': 'parent'},
    )
    child_name = models.CharField(max_length=120, help_text='Student name on the invoice')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # stored in pence so we match stripe unit_amount (e.g. 25000 = £250.00)
    amount_pence = models.PositiveIntegerField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OUTSTANDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-due_date']

    def __str__(self):
        return f'{self.title} — {self.child_name}'

    @property
    def amount_display(self):
        """Human-readable GBP for templates."""
        return f'£{self.amount_pence / 100:.2f}'


class Payment(models.Model):
    """One completed (or failed) Stripe Checkout session."""

    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_FAILED, 'Failed'),
    ]

    fee_item = models.ForeignKey(FeeItem, on_delete=models.PROTECT, related_name='payments')
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    stripe_session_id = models.CharField(max_length=255, unique=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True)
    amount_pence = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, default='GBP')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    receipt_reference = models.CharField(max_length=32, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment #{self.pk} — {self.fee_item.title} ({self.status})'

    @property
    def amount_display(self):
        return f'£{self.amount_pence / 100:.2f}'

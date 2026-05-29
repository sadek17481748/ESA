"""payments/admin.py — fees and payment records in admin."""
from django.contrib import admin

from .models import FeeItem, Payment, SubscriptionPayment


@admin.register(FeeItem)
class FeeItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'child_name', 'school', 'parent', 'amount_display', 'due_date', 'status')
    list_filter = ('status', 'school')
    search_fields = ('title', 'child_name', 'parent__username')
    raw_id_fields = ('school', 'parent')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('fee_item', 'parent', 'amount_display', 'status', 'receipt_reference', 'paid_at')
    list_filter = ('status',)
    search_fields = ('stripe_session_id', 'receipt_reference')
    readonly_fields = ('stripe_session_id', 'stripe_payment_intent', 'created_at')


@admin.register(SubscriptionPayment)
class SubscriptionPaymentAdmin(admin.ModelAdmin):
    list_display = ('school', 'tier', 'admin', 'amount_display', 'status', 'paid_at')
    list_filter = ('status', 'tier', 'school')
    search_fields = ('receipt_reference', 'stripe_session_id')

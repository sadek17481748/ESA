"""
schools/admin.py
Admin screens for managing tenant schools.
"""
from django.contrib import admin

from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscription_tier', 'status', 'stripe_account_id', 'created_at')
    list_filter = ('subscription_tier', 'status')
    search_fields = ('name', 'contact_email')

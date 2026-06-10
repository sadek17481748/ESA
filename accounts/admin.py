"""
accounts/admin.py
Django admin config for User — shows role and school on the list screen.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailVerificationCode, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'email_verified', 'role', 'school', 'is_active', 'is_staff')
    list_filter = ('role', 'school', 'email_verified', 'is_active', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('ESA', {'fields': ('role', 'school', 'email_verified', 'notify_on_messages')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('ESA', {'fields': ('role', 'school')}),
    )


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_used',)

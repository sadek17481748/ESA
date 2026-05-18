"""
audit/signals.py
Hooks Django login/logout to write audit rows automatically.
"""
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import AuditLog
from .services import log_action


@receiver(user_logged_in)
def audit_login(sender, request, user, **kwargs):
    log_action(
        user=user,
        action=AuditLog.ACTION_LOGIN,
        resource='Session',
        detail='User logged in',
        request=request,
    )


@receiver(user_logged_out)
def audit_logout(sender, request, user, **kwargs):
    log_action(
        user=user,
        action=AuditLog.ACTION_LOGOUT,
        resource='Session',
        detail='User logged out',
        request=request,
    )

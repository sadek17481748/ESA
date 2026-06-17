"""
audit/services.py
Single entry point for writing audit rows from views and signals.
"""
from .models import AuditLog


def log_action(*, user, action, resource='', resource_id='', detail='', request=None):
    """
    Create an AuditLog row. Pass request when you have it so we capture IP + tenant.
    """
    school = None
    if user and user.is_authenticated:
        school = user.school
    if request and getattr(request, 'tenant_school', None):
        school = request.tenant_school

    ip = None
    if request:
        ip = request.META.get('REMOTE_ADDR')

    return AuditLog.objects.create(
        school=school,
        user=user if user and user.is_authenticated else None,
        action=action,
        resource=resource,
        resource_id=str(resource_id) if resource_id else '',
        detail=detail,
        ip_address=ip,
    )

"""Write audit rows for sensitive actions."""

from .models import AuditLog


def log_action(*, user, action, resource='', resource_id='', detail='', request=None):
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


# bug: school was always None because we read user.school before checking tenant_school on request
# AuditLog.objects.create(school=None, user=user, action=action, ...)

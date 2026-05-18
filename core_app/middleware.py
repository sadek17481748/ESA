"""
core_app/middleware.py
Sets request.tenant_school after auth so views and audit can read it.
"""


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.tenant_school = None
        user = getattr(request, 'user', None)
        if user and user.is_authenticated and user.school_id:
            request.tenant_school = user.school
        return self.get_response(request)

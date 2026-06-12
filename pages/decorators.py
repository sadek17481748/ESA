"""pages/decorators.py — role gates for portal views."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect


def _wants_json(request):
    """True when the client expects a JSON API response (fetch from timetable builder, etc.)."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    content_type = request.content_type or ''
    return content_type.startswith('application/json')


def role_required(*roles):
    """Restrict a view to specific user.role values."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                if _wants_json(request):
                    return JsonResponse(
                        {'error': 'Only school admins can perform this action.'},
                        status=403,
                    )
                return redirect('pages:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

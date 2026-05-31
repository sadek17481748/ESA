"""pages/decorators.py — role gates for portal views."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    """Restrict a view to specific user.role values."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                return redirect('pages:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

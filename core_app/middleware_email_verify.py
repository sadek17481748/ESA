"""Redirect unverified users to email verification before using the portal."""
from django.shortcuts import redirect
from django.urls import reverse

from accounts.verification import user_needs_email_verification

# Paths that do not require a verified email
ALLOWED_PREFIXES = (
    '/accounts/login',
    '/accounts/logout',
    '/accounts/password-reset',
    '/accounts/verify-email',
    '/register',
    '/link/',
    '/admin/',
    '/api/',
    '/css/',
    '/static/',
    '/media/',
)


class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and user_needs_email_verification(user):
            path = request.path
            if path == '/' or not any(path.startswith(p) for p in ALLOWED_PREFIXES):
                return redirect(reverse('verify_email'))
        return self.get_response(request)

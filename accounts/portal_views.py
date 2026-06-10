"""
accounts/portal_views.py
Password recovery and email verification (session portal).
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_POST

from core_app.email_service import send_user_email

from .forms_portal import EsaPasswordResetForm, EmailVerificationForm
from .verification import create_and_send_verification_code, user_needs_email_verification, verify_email_code

User = get_user_model()


class EsaPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.txt'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = EsaPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = list(User.objects.filter(email__iexact=email, is_active=True))
        if not users:
            return super().form_valid(form)

        for user in users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_path = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = self.request.build_absolute_uri(reset_path)
            body = (
                f'Hello {user.first_name or user.username},\n\n'
                f'Reset your ESA password using this link (valid for a limited time):\n\n'
                f'{reset_url}\n\n'
                f'If you did not request this, ignore this email.\n'
            )
            send_user_email('[ESA] Password reset', body, [user.email])

        return redirect(self.success_url)


class EsaPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class EsaPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class EsaPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


@login_required
def verify_email(request):
    from django.utils import timezone

    user = request.user
    if not user_needs_email_verification(user):
        return redirect('pages:dashboard')

    dev_code = None
    form = EmailVerificationForm()

    if request.method == 'POST':
        if request.POST.get('action') == 'resend':
            dev_code, sent = create_and_send_verification_code(user, request=request)
            if sent:
                messages.success(request, f'Verification code sent to {user.email}.')
            else:
                messages.info(request, 'Email is not configured — use the code shown below (dev only).')
        else:
            form = EmailVerificationForm(request.POST)
            if form.is_valid():
                ok, msg = verify_email_code(user, form.cleaned_data['code'])
                if ok:
                    messages.success(request, msg)
                    return redirect('pages:dashboard')
                messages.error(request, msg)
    elif not user.email_codes.filter(is_used=False, expires_at__gte=timezone.now()).exists():
        dev_code, _ = create_and_send_verification_code(user, request=request)

    return render(request, 'registration/verify_email.html', {
        'form': form,
        'email': user.email,
        'dev_code': dev_code if settings.DEBUG else None,
    })


"""
pages/views.py
Portal UI — web registration.
"""
from django.contrib.auth import login
from django.shortcuts import redirect, render

from audit.models import AuditLog
from audit.services import log_action

from .forms import RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(
                user=user, action=AuditLog.ACTION_CREATE, resource='User',
                resource_id=user.pk, detail=f'Web registration as {user.role}', request=request,
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

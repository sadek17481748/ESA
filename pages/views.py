"""
pages/views.py
Portal UI — login redirect, registration, dashboards, and placeholder feature pages.
"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from audit.models import AuditLog
from audit.services import log_action

from .forms import EsaAuthenticationForm, RegisterForm

# Maps user.role to the dashboard they land on after login
ROLE_DASHBOARD = {
    'super_admin': 'pages:dashboard_super_admin',
    'school_admin': 'pages:dashboard_school_admin',
    'teacher': 'pages:dashboard_teacher',
    'student': 'pages:dashboard_student',
    'parent': 'pages:dashboard_parent',
}


def dashboard_router(request):
    """Send logged-in users to the right dashboard."""
    if not request.user.is_authenticated:
        return redirect('login')
    url_name = ROLE_DASHBOARD.get(request.user.role, 'home')
    return redirect(url_name)


def register(request):
    """Create account — parent or student linked to a school."""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(
                user=user,
                action=AuditLog.ACTION_CREATE,
                resource='User',
                resource_id=user.pk,
                detail=f'Web registration as {user.role}',
                request=request,
            )
            login(request, user)
            return redirect('pages:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class EsaLoginView(LoginView):
    """Session login styled like the wireframe."""

    template_name = 'registration/login.html'
    authentication_form = EsaAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('pages:dashboard')


def _placeholder(request, template_name, page_title, page_meta=''):
    return render(request, template_name, {
        'page_title': page_title,
        'page_meta': page_meta or 'Placeholder — data wiring comes later.',
    })


@login_required
def dashboard_parent(request):
    return _placeholder(
        request, 'pages/dashboard/parent.html',
        'Parent portal', 'Verified progress and school home communication.',
    )


@login_required
def dashboard_teacher(request):
    return _placeholder(
        request, 'pages/dashboard/teacher.html',
        'Teacher workspace', "Today's sessions, assignments, and verification queues.",
    )


@login_required
def dashboard_student(request):
    return _placeholder(
        request, 'pages/dashboard/student.html',
        'Student portal', 'Timetable, homework, and progress in one place.',
    )


@login_required
def dashboard_school_admin(request):
    return _placeholder(
        request, 'pages/dashboard/school_admin.html',
        'School admin', 'Staff, classes, fees, and school settings.',
    )


@login_required
def dashboard_super_admin(request):
    return _placeholder(
        request, 'pages/dashboard/super_admin.html',
        'Platform admin', 'Schools, subscriptions, and platform analytics.',
    )


@login_required

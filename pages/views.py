"""
pages/views.py
Portal UI — login redirect, registration, dashboards, and placeholder feature pages.
"""
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from audit.models import AuditLog
from audit.services import log_action

from .forms import EsaAuthenticationForm, RegisterForm, SchoolRegisterForm, active_schools

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
    """Parent or student sign-up — pick a school from the list."""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    has_schools = active_schools().exists()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(
                user=user,
                action=AuditLog.ACTION_CREATE,
                resource='User',
                resource_id=user.pk,
                detail=f'Web registration as {user.role} at {user.school.name}',
                request=request,
            )
            login(request, user)
            return redirect('pages:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {
        'form': form,
        'has_schools': has_schools,
    })


def register_school(request):
    """Register a new school — adds it to the parent/student school picker."""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    if request.method == 'POST':
        form = SchoolRegisterForm(request.POST)
        if form.is_valid():
            school, user = form.save()
            log_action(
                user=user,
                action=AuditLog.ACTION_CREATE,
                resource='School',
                resource_id=school.pk,
                detail=f'Web school registration: {school.name}',
                request=request,
            )
            login(request, user)
            return redirect('pages:dashboard')
    else:
        form = SchoolRegisterForm()
    return render(request, 'registration/register_school.html', {'form': form})


class EsaLoginView(LoginView):
    """Session login styled like the wireframe."""

    template_name = 'registration/login.html'
    authentication_form = EsaAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('pages:dashboard')


def logout_view(request):
    """Log out and return to the landing page (works from nav links)."""
    logout(request)
    return redirect('home')


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
def page_attendance(request):
    return _placeholder(request, 'pages/features/attendance.html', 'Attendance')


@login_required
def page_behaviour(request):
    return _placeholder(request, 'pages/features/behaviour.html', 'Behaviour')


@login_required
def page_exams(request):
    return _placeholder(request, 'pages/features/exams.html', 'Exams')


@login_required
def page_hifz(request):
    return _placeholder(request, 'pages/features/hifz_progress.html', 'Hifz progress')


@login_required
def page_messages(request):
    return _placeholder(request, 'pages/features/messages.html', 'Messages')


@login_required
def page_payments_info(request):
    return _placeholder(request, 'pages/features/payments_info.html', 'Payments overview')


@login_required
def page_quran(request):
    return _placeholder(request, 'pages/features/quran_annotation.html', 'Qur’an annotation')


@login_required
def page_subscription(request):
    return _placeholder(request, 'pages/features/subscription.html', 'Subscription plans')


@login_required
def page_timetable(request):
    return _placeholder(request, 'pages/features/timetable.html', 'Timetable')


@login_required
def page_worksheets(request):
    return _placeholder(request, 'pages/features/worksheets.html', 'Worksheets & homework')


@login_required
def page_analytics(request):
    return _placeholder(request, 'pages/features/analytics.html', 'Analytics')

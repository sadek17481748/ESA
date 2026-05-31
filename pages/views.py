"""
pages/views.py
Portal UI — login redirect, registration, dashboards, and placeholder feature pages.
"""
import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from academics.models import ClassGroup
from audit.models import AuditLog
from audit.services import log_action
from teachers.models import TeacherProfile

from .decorators import role_required
from .forms import AddTeacherForm, EsaAuthenticationForm, RegisterForm, SchoolRegisterForm, active_schools
from .portal import build_portal_context
from .super_admin_stats import build_super_admin_dashboard_context
from .timetable_service import PERIODS, WEEKDAYS, build_timetable_grid, ensure_school_subjects, save_timetable

ROLE_DASHBOARD = {
    'super_admin': 'pages:dashboard_super_admin',
    'school_admin': 'pages:dashboard_school_admin',
    'teacher': 'pages:dashboard_teacher',
    'student': 'pages:dashboard_student',
    'parent': 'pages:dashboard_parent',
}


def dashboard_router(request):
    if not request.user.is_authenticated:
        return redirect('login')
    url_name = ROLE_DASHBOARD.get(request.user.role, 'home')
    return redirect(url_name)


def register(request):
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
    template_name = 'registration/login.html'
    authentication_form = EsaAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('pages:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(
            user=self.request.user,
            action=AuditLog.ACTION_LOGIN,
            resource='User',
            resource_id=self.request.user.pk,
            detail='Session login',
            request=self.request,
        )
        return response


def logout_view(request):
    logout(request)
    return redirect('home')


def _portal_page(request, template_name, page_title, page_meta=''):
    ctx = build_portal_context(request, page_title, page_meta)
    return render(request, template_name, ctx)


@login_required
def dashboard_parent(request):
    return _portal_page(
        request, 'pages/dashboard/parent.html',
        'Parent overview', 'Progress, attendance, and fees for your children.',
    )


@login_required
def dashboard_teacher(request):
    return _portal_page(
        request, 'pages/dashboard/teacher.html',
        'Teacher workspace', "Today's sessions, assignments, and verification queues.",
    )


@login_required
def dashboard_student(request):
    return _portal_page(
        request, 'pages/dashboard/student.html',
        'Student overview', 'Timetable, homework, and progress in one place.',
    )


@login_required
def dashboard_school_admin(request):
    school = request.user.school
    teachers = TeacherProfile.objects.filter(school=school).select_related('user') if school else []
    ctx = build_portal_context(
        request,
        'School overview',
        'Staff, classes, fees, and settings for your school.',
    )
    ctx['teachers'] = teachers
    ctx['teacher_count'] = teachers.count()
    return render(request, 'pages/dashboard/school_admin.html', ctx)


@role_required('school_admin')
def school_admin_teachers(request):
    school = request.user.school
    ctx = build_portal_context(request, 'Teachers', 'Staff accounts at your school.')
    ctx['teachers'] = TeacherProfile.objects.filter(school=school).select_related('user')
    return render(request, 'pages/school_admin/teachers.html', ctx)


@role_required('school_admin')
def school_admin_add_teacher(request):
    school = request.user.school
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            user, profile = form.save(school)
            log_action(
                user=request.user,
                action=AuditLog.ACTION_CREATE,
                resource='TeacherProfile',
                resource_id=profile.pk,
                detail=f'Created teacher {user.username}',
                request=request,
            )
            return redirect('pages:school_admin_teachers')
    else:
        form = AddTeacherForm()
    ctx = build_portal_context(
        request,
        'Add teacher',
        'Create login details — teachers can manage timetables, homework, registers, and Hifz/Alimiyah work.',
    )
    ctx['form'] = form
    return render(request, 'pages/school_admin/add_teacher.html', ctx)


def _teacher_profile_for_user(user):
    if user.role != 'teacher':
        return None
    return TeacherProfile.objects.filter(user=user).first()


@role_required('school_admin', 'teacher')
def page_timetable(request):
    school = request.user.school
    ensure_school_subjects(school)
    classes = ClassGroup.objects.filter(school=school).select_related(
        'teacher', 'teacher__user', 'year_group',
    )
    class_id = request.GET.get('class')
    if class_id:
        class_group = get_object_or_404(ClassGroup, pk=class_id, school=school)
    else:
        class_group = classes.first()

    teacher_profile = _teacher_profile_for_user(request.user)
    if request.user.role == 'teacher' and teacher_profile:
        if class_group and class_group.teacher_id != teacher_profile.pk:
            owned = classes.filter(teacher=teacher_profile).first()
            if owned:
                class_group = owned

    subjects = ensure_school_subjects(school)
    grid = build_timetable_grid(class_group) if class_group else {}

    periods = [
        {'start': s.strftime('%H:%M'), 'end': e.strftime('%H:%M'), 'label': s.strftime('%H:%M')}
        for s, e in PERIODS
    ]
    weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    ctx = build_portal_context(
        request,
        'Timetable',
        'Drag subjects onto the grid — saved for your school with class and teacher.',
    )
    ctx.update({
        'classes': classes,
        'class_group': class_group,
        'subjects': subjects,
        'periods': periods,
        'weekdays': WEEKDAYS,
        'weekday_labels': weekday_labels,
        'grid_json': json.dumps({f'{w}-{t}': v for (w, t), v in grid.items()}) if class_group else '{}',
        'can_edit': request.user.role == 'school_admin' or teacher_profile is not None,
    })
    return render(request, 'pages/features/timetable.html', ctx)


@role_required('school_admin', 'teacher')
@require_POST
def timetable_save(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    class_group = get_object_or_404(ClassGroup, pk=payload.get('class_group_id'), school=school)
    teacher_profile = _teacher_profile_for_user(request.user)
    if request.user.role == 'teacher' and class_group.teacher_id != teacher_profile.pk:
        return JsonResponse({'error': 'Not allowed for this class'}, status=403)
    if not teacher_profile and request.user.role == 'school_admin':
        teacher_profile = class_group.teacher

    slots = payload.get('slots', [])
    save_timetable(class_group, teacher_profile, slots)
    log_action(
        user=request.user,
        action=AuditLog.ACTION_UPDATE,
        resource='TimetableSlot',
        resource_id=class_group.pk,
        detail=f'Saved timetable for {class_group.name}',
        request=request,
    )
    return JsonResponse({'ok': True, 'count': len(slots)})


@role_required('super_admin')
def dashboard_super_admin(request):
    ctx = build_super_admin_dashboard_context()
    ctx.update(build_portal_context(
        request,
        'Platform overview',
        'Live view of schools, subscriptions, users, and platform activity.',
    ))
    return render(request, 'pages/dashboard/super_admin.html', ctx)


@login_required
def page_attendance(request):
    return _portal_page(request, 'pages/features/attendance.html', 'Attendance')


@login_required
def page_behaviour(request):
    return _portal_page(request, 'pages/features/behaviour.html', 'Behaviour')


@login_required
def page_exams(request):
    return _portal_page(request, 'pages/features/exams.html', 'Exams')


@login_required
def page_hifz(request):
    return _portal_page(request, 'pages/features/hifz_progress.html', 'Hifz progress')


@login_required
def page_messages(request):
    return _portal_page(request, 'pages/features/messages.html', 'Messages')


@login_required
def page_payments_info(request):
    return _portal_page(request, 'pages/features/payments_info.html', 'Payments overview')


@login_required
def page_quran(request):
    return _portal_page(request, 'pages/features/quran_annotation.html', 'Qur’an annotation')


@login_required
def page_subscription(request):
    return _portal_page(request, 'pages/features/subscription.html', 'Subscription plans')


@login_required
def page_worksheets(request):
    return _portal_page(request, 'pages/features/worksheets.html', 'Worksheets & homework')


@login_required
def page_analytics(request):
    return _portal_page(request, 'pages/features/analytics.html', 'Analytics')

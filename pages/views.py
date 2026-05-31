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

from timetable.models import Timetable

from .decorators import role_required
from .forms import (
    AddTeacherForm,
    CreateSubjectForm,
    EsaAuthenticationForm,
    RegisterForm,
    SchoolRegisterForm,
    TimetableForm,
    active_schools,
)
from .portal import build_portal_context
from .super_admin_stats import build_super_admin_dashboard_context
from .timetable_service import (
    PERIODS,
    WEEKDAYS,
    build_timetable_grid,
    create_subject,
    create_timetable,
    get_or_create_default_timetable,
    list_school_subjects,
    list_timetables,
    rename_timetable,
    save_timetable,
    teachers_for_json,
    user_can_edit_timetable,
)

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
    teacher_profile = _teacher_profile_for_user(request.user)
    classes = ClassGroup.objects.filter(school=school).select_related(
        'teacher', 'teacher__user', 'year_group',
    )
    class_id = request.GET.get('class')
    if class_id:
        class_group = get_object_or_404(ClassGroup, pk=class_id, school=school)
    else:
        class_group = classes.first()

    if request.user.role == 'teacher' and teacher_profile and class_group:
        if class_group.teacher_id != teacher_profile.pk:
            owned = classes.filter(teacher=teacher_profile).first()
            if owned:
                class_group = owned

    timetables = list(list_timetables(school, class_group))
    timetable_id = request.GET.get('timetable')
    timetable = None
    if timetable_id:
        timetable = get_object_or_404(Timetable, pk=timetable_id, school=school)
        if timetable.class_group_id and class_group and timetable.class_group_id != class_group.pk:
            class_group = timetable.class_group
    elif timetables:
        timetable = timetables[0]
    elif class_group:
        timetable = get_or_create_default_timetable(school, class_group)
        timetables = list(list_timetables(school, class_group))

    if timetable and not class_group and timetable.class_group_id:
        class_group = timetable.class_group

    subjects = list_school_subjects(school)
    teachers = teachers_for_json(school)
    grid = build_timetable_grid(timetable) if timetable else {}

    periods = [
        {'start': s.strftime('%H:%M'), 'end': e.strftime('%H:%M'), 'label': s.strftime('%H:%M')}
        for s, e in PERIODS
    ]
    weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    can_edit = timetable and user_can_edit_timetable(request.user, timetable, teacher_profile)

    ctx = build_portal_context(
        request,
        'Timetable',
        'Create and edit multiple timetables — assign subjects and teachers to each slot.',
    )
    ctx.update({
        'classes': classes,
        'class_group': class_group,
        'timetables': timetables,
        'timetable': timetable,
        'subjects': subjects,
        'teachers_json': json.dumps(teachers),
        'periods': periods,
        'weekdays': WEEKDAYS,
        'weekday_labels': weekday_labels,
        'grid_json': json.dumps({f'{w}-{t}': v for (w, t), v in grid.items()}) if timetable else '{}',
        'can_edit': can_edit,
        'can_manage_timetables': request.user.role == 'school_admin',
        'timetable_form': TimetableForm(school),
        'subject_form': CreateSubjectForm(),
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

    timetable = get_object_or_404(Timetable, pk=payload.get('timetable_id'), school=school)
    teacher_profile = _teacher_profile_for_user(request.user)
    if not user_can_edit_timetable(request.user, timetable, teacher_profile):
        return JsonResponse({'error': 'Not allowed for this timetable'}, status=403)

    class_group = timetable.class_group
    if not class_group:
        class_group = get_object_or_404(
            ClassGroup, pk=payload.get('class_group_id'), school=school,
        )

    slots = payload.get('slots', [])
    save_timetable(timetable, class_group, slots)
    log_action(
        user=request.user,
        action=AuditLog.ACTION_UPDATE,
        resource='Timetable',
        resource_id=timetable.pk,
        detail=f'Saved timetable {timetable.name}',
        request=request,
    )
    return JsonResponse({'ok': True, 'count': len(slots)})


@role_required('school_admin', 'teacher')
@require_POST
def timetable_create(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = (payload.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)

    class_group = None
    class_group_id = payload.get('class_group_id')
    if class_group_id:
        class_group = get_object_or_404(ClassGroup, pk=class_group_id, school=school)

    if Timetable.objects.filter(school=school, name=name).exists():
        return JsonResponse({'error': 'A timetable with that name already exists'}, status=400)

    timetable = create_timetable(
        school,
        name=name,
        class_group=class_group,
        notes=payload.get('notes', ''),
    )
    log_action(
        user=request.user,
        action=AuditLog.ACTION_CREATE,
        resource='Timetable',
        resource_id=timetable.pk,
        detail=f'Created timetable {timetable.name}',
        request=request,
    )
    return JsonResponse({
        'ok': True,
        'timetable': {
            'id': timetable.pk,
            'name': timetable.name,
            'class_group_id': timetable.class_group_id,
        },
    })


@role_required('school_admin', 'teacher')
@require_POST
def timetable_update(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    timetable = get_object_or_404(Timetable, pk=payload.get('timetable_id'), school=school)
    teacher_profile = _teacher_profile_for_user(request.user)
    if not user_can_edit_timetable(request.user, timetable, teacher_profile):
        return JsonResponse({'error': 'Not allowed'}, status=403)

    name = (payload.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)

    if Timetable.objects.filter(school=school, name=name).exclude(pk=timetable.pk).exists():
        return JsonResponse({'error': 'A timetable with that name already exists'}, status=400)

    rename_timetable(timetable, name=name, notes=payload.get('notes'))
    return JsonResponse({'ok': True, 'name': timetable.name})


@role_required('school_admin')
@require_POST
def timetable_delete(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    timetable = get_object_or_404(Timetable, pk=payload.get('timetable_id'), school=school)
    name = timetable.name
    timetable.is_active = False
    timetable.save(update_fields=['is_active'])
    log_action(
        user=request.user,
        action=AuditLog.ACTION_DELETE,
        resource='Timetable',
        resource_id=timetable.pk,
        detail=f'Archived timetable {name}',
        request=request,
    )
    return JsonResponse({'ok': True})


@role_required('school_admin', 'teacher')
@require_POST
def subject_create(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = (payload.get('name') or '').strip()
    if not name:
        return JsonResponse({'error': 'Subject name is required'}, status=400)

    track = payload.get('track', 'general')
    if track not in ('general', 'hifz', 'alimiyah'):
        track = 'general'

    try:
        subject = create_subject(
            school,
            name=name,
            track=track,
            code=(payload.get('code') or '').strip(),
        )
    except ValueError as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    log_action(
        user=request.user,
        action=AuditLog.ACTION_CREATE,
        resource='Subject',
        resource_id=subject.pk,
        detail=f'Created subject {subject.name}',
        request=request,
    )
    return JsonResponse({
        'ok': True,
        'subject': {
            'id': subject.pk,
            'name': subject.name,
            'track': subject.track,
        },
    })


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

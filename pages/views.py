"""
pages/views.py
Portal UI — login redirect, registration, dashboards, and placeholder feature pages.
"""
import json
from datetime import datetime

from django.contrib import messages
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

from .attendance_service import (
    build_class_register,
    build_school_attendance_overview,
    parent_children_attendance,
    save_class_register,
    session_date_or_today,
    student_attendance_history,
    teacher_classes,
)
from .decorators import role_required
from .enrollment_service import (
    enroll_student,
    student_needs_class,
    student_portal_context,
    student_profile_for_user,
)
from .forms import (
    AddTeacherForm,
    BehaviourLogForm,
    CreateSubjectForm,
    EsaAuthenticationForm,
    PickClassForm,
    RegisterForm,
    SchoolRegisterForm,
    TimetableForm,
    active_schools,
)
from .portal import build_portal_context
from .parent_dashboard_service import parent_children_summary
from .analytics_service import school_analytics
from .behaviour_service import (
    behaviour_for_parent,
    behaviour_for_school_admin,
    behaviour_for_teacher,
)
from academics.models import BehaviourRecord
from .super_admin_stats import build_super_admin_dashboard_context
from .timetable_service import (
    PERIODS,
    WEEKDAYS,
    build_timetable_grid,
    create_subject,
    create_timetable,
    get_or_create_default_timetable,
    list_live_timetables,
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


def register_classes(request):
    """Public JSON — classes for a school (registration class picker)."""
    school_id = request.GET.get('school')
    if not school_id:
        return JsonResponse({'classes': []})
    classes = ClassGroup.objects.filter(school_id=school_id).order_by('name')
    return JsonResponse({
        'classes': [{'id': c.pk, 'name': c.name} for c in classes],
    })


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
            from accounts.verification import create_and_send_verification_code, user_needs_email_verification
            if user_needs_email_verification(user):
                create_and_send_verification_code(user, request=request)
                messages.info(request, f'We sent a verification code to {user.email}.')
                return redirect('verify_email')
            return redirect('pages:dashboard')
    else:
        initial = {}
        if request.GET.get('code'):
            initial['link_code'] = request.GET.get('code').strip().upper()
            initial['role'] = 'parent'
        if request.GET.get('school'):
            initial['school'] = request.GET.get('school')
        form = RegisterForm(initial=initial)
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
            from messaging.notifications import notify_platform_school_registration
            notify_platform_school_registration(school, user)
            login(request, user)
            from accounts.verification import create_and_send_verification_code, user_needs_email_verification
            if user_needs_email_verification(user):
                create_and_send_verification_code(user, request=request)
                messages.info(request, f'We sent a verification code to {user.email}.')
                return redirect('verify_email')
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
        from accounts.verification import user_needs_email_verification
        if user_needs_email_verification(self.request.user):
            from django.contrib import messages
            messages.info(self.request, 'Please verify your email to continue.')
            from django.shortcuts import redirect
            from django.urls import reverse
            return redirect(reverse('verify_email'))
        return response


def logout_view(request):
    logout(request)
    return redirect('home')


def _portal_page(request, template_name, page_title, page_meta=''):
    ctx = build_portal_context(request, page_title, page_meta)
    return render(request, template_name, ctx)


@login_required
def pick_class(request):
    """Students without a class enrolment pick their class."""
    if request.user.role != 'student':
        return redirect('pages:dashboard')
    profile = student_profile_for_user(request.user)
    if not profile or not student_needs_class(request.user):
        return redirect('pages:dashboard')

    if request.method == 'POST':
        form = PickClassForm(request.user.school, request.POST)
        if form.is_valid():
            enroll_student(profile, form.cleaned_data['class_group'])
            messages.success(request, f'You are now enrolled in {form.cleaned_data["class_group"].name}.')
            return redirect('pages:dashboard_student')
    else:
        form = PickClassForm(request.user.school)

    return render(request, 'registration/pick_class.html', {
        'form': form,
        'school_name': request.user.school.name if request.user.school else '',
    })


@login_required
def dashboard_parent(request):
    session_date = session_date_or_today(request.GET.get('date'))
    children = parent_children_summary(request.user, session_date)
    ctx = build_portal_context(
        request,
        'Parent overview',
        'Attendance and progress for your children.',
    )
    ctx.update({'children': children, 'session_date': session_date})
    return render(request, 'pages/dashboard/parent.html', ctx)


@login_required
def dashboard_teacher(request):
    school = request.user.school
    teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
    classes = list(teacher_classes(school, teacher_profile))
    primary_class = classes[0] if classes else None
    ctx = build_portal_context(
        request,
        'Teacher workspace',
        "Take today's register and manage your classes.",
    )
    ctx.update({
        'teacher_classes': classes,
        'primary_class': primary_class,
    })
    return render(request, 'pages/dashboard/teacher.html', ctx)


@login_required
def dashboard_student(request):
    if student_needs_class(request.user):
        return redirect('pages:pick_class')
    profile = student_profile_for_user(request.user)
    portal = student_portal_context(profile) if profile else {}
    ctx = build_portal_context(
        request,
        'Student overview',
        'Your class timetable, homework, and progress.',
    )
    ctx.update(portal)
    return render(request, 'pages/dashboard/student.html', ctx)


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
        'live_timetables': list_live_timetables(school),
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
        'can_add_class': request.user.role == 'school_admin',
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


@role_required('school_admin')
@require_POST
def class_create(request):
    school = request.user.school
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from .forms import AddClassForm
    form = AddClassForm(school, payload)
    if not form.is_valid():
        errors = '; '.join(
            f'{field}: {msgs[0]}' for field, msgs in form.errors.items()
        )
        return JsonResponse({'error': errors or 'Invalid class details'}, status=400)

    if ClassGroup.objects.filter(school=school, name=form.cleaned_data['name']).exists():
        return JsonResponse({'error': 'A class with that name already exists'}, status=400)

    class_group = form.save(school)
    get_or_create_default_timetable(school, class_group)
    log_action(
        user=request.user,
        action=AuditLog.ACTION_CREATE,
        resource='ClassGroup',
        resource_id=class_group.pk,
        detail=f'Created class {class_group.name}',
        request=request,
    )
    return JsonResponse({
        'ok': True,
        'class': {
            'id': class_group.pk,
            'name': class_group.name,
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
    school = request.user.school
    role = request.user.role

    if role == 'school_admin':
        session_date = session_date_or_today(_parse_date_param(request.GET.get('date')))
        overview, totals, session_date = build_school_attendance_overview(school, session_date)
        ctx = build_portal_context(
            request,
            'Attendance',
            'All students grouped by class — track registers across your school.',
        )
        ctx.update({
            'overview': overview,
            'totals': totals,
            'session_date': session_date,
        })
        return render(request, 'pages/features/attendance_admin.html', ctx)

    if role == 'teacher':
        teacher_profile = TeacherProfile.objects.filter(user=request.user).first()
        classes = list(teacher_classes(school, teacher_profile))
        class_id = request.GET.get('class')
        if class_id:
            class_group = get_object_or_404(ClassGroup, pk=class_id, school=school)
        else:
            class_group = classes[0] if classes else None

        session_date = session_date_or_today(_parse_date_param(request.GET.get('date')))
        register = build_class_register(class_group, session_date) if class_group else None

        if request.method == 'POST' and class_group:
            marks_payload = {}
            for key, value in request.POST.items():
                if key.startswith('status_'):
                    student_id = key.replace('status_', '')
                    marks_payload[student_id] = {'status': value}
            session, count = save_class_register(
                school, class_group, session_date, request.user, marks_payload,
            )
            log_action(
                user=request.user,
                action=AuditLog.ACTION_UPDATE,
                resource='AttendanceSession',
                resource_id=session.pk,
                detail=f'Saved register for {class_group.name} ({count} marks)',
                request=request,
            )
            messages.success(request, f'Register saved for {class_group.name}.')
            return redirect(
                f'{reverse("pages:attendance")}?class={class_group.pk}&date={session_date.isoformat()}',
            )

        ctx = build_portal_context(
            request,
            'Take register',
            'Mark each student present, late, or absent for today.',
        )
        ctx.update({
            'classes': classes,
            'class_group': class_group,
            'register': register,
            'session_date': session_date,
        })
        return render(request, 'pages/features/attendance_register.html', ctx)

    if role == 'student':
        if student_needs_class(request.user):
            return redirect('pages:pick_class')
        profile = student_profile_for_user(request.user)
        history = student_attendance_history(profile) if profile else []
        ctx = build_portal_context(request, 'My attendance', 'Your attendance record.')
        ctx.update({'history': history, 'student': profile})
        return render(request, 'pages/features/attendance_student.html', ctx)

    if role == 'parent':
        session_date = session_date_or_today(_parse_date_param(request.GET.get('date')))
        children = parent_children_attendance(request.user, session_date)
        ctx = build_portal_context(request, 'Attendance', 'Attendance for your children.')
        ctx.update({'children': children, 'session_date': session_date})
        return render(request, 'pages/features/attendance_student.html', ctx)

    return _portal_page(request, 'pages/features/attendance.html', 'Attendance')


def _parse_date_param(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


@login_required
def page_behaviour(request):
    user = request.user
    school = user.school
    form = None
    records = []

    if user.role == 'teacher' and school:
        if request.method == 'POST':
            form = BehaviourLogForm(school, user, request.POST)
            if form.is_valid():
                BehaviourRecord.objects.create(
                    school=school,
                    student=form.cleaned_data['student'],
                    teacher=user,
                    record_type=form.cleaned_data['record_type'],
                    title=form.cleaned_data['title'],
                    notes=form.cleaned_data.get('notes', ''),
                )
                messages.success(request, 'Behaviour record saved.')
                return redirect('pages:behaviour')
        else:
            form = BehaviourLogForm(school, user)
        records = behaviour_for_teacher(user)
    elif user.role == 'parent':
        records = behaviour_for_parent(user)
    elif user.role == 'school_admin' and school:
        records = behaviour_for_school_admin(school)

    ctx = build_portal_context(request, 'Behaviour', 'Commendations and incidents.')
    ctx.update({'records': records, 'form': form})
    return render(request, 'pages/features/behaviour.html', ctx)


@login_required
def page_exams(request):
    from exams.views import exams_list
    return exams_list(request)


@login_required
def page_hifz(request):
    return _portal_page(request, 'pages/features/hifz_progress.html', 'Hifz progress')


@login_required
def page_payments_info(request):
    return _portal_page(request, 'pages/features/payments_info.html', 'Payments overview')


@login_required
def page_quran(request):
    from quran.views import quran_list
    return quran_list(request)


@login_required
def page_subscription(request):
    if request.user.role == 'school_admin':
        return redirect('payments:subscription')
    return _portal_page(
        request,
        'pages/features/subscription.html',
        'Subscription plans',
        'Only school admins can manage subscriptions.',
    )


@login_required
def page_worksheets(request):
    from lms.views import lms_student_worksheets
    return lms_student_worksheets(request)


@login_required
@role_required('school_admin')
def page_analytics(request):
    school = request.user.school
    stats = school_analytics(school) if school else {}
    ctx = build_portal_context(request, 'Analytics', 'School KPIs and overview.')
    ctx['stats'] = stats
    return render(request, 'pages/features/analytics.html', ctx)


@role_required('school_admin')
def school_admin_students(request):
    from students.link_service import build_parent_link_url, get_or_create_active_code
    from students.models import StudentProfile

    school = request.user.school
    students = StudentProfile.objects.filter(school=school, is_active=True).order_by(
        'last_name', 'first_name',
    )
    rows = []
    for student in students:
        code_row = get_or_create_active_code(student=student, created_by=request.user)
        rows.append({
            'student': student,
            'code': code_row,
            'link_url': build_parent_link_url(request, code_row.code),
        })
    ctx = build_portal_context(
        request,
        'Students & parent links',
        'Issue a unique code so parents can link to each student.',
    )
    ctx['rows'] = rows
    return render(request, 'pages/school_admin/students.html', ctx)


@role_required('school_admin')
@require_POST
def school_admin_regenerate_link_code(request, student_id):
    from students.link_service import regenerate_link_code
    from students.models import StudentProfile

    student = get_object_or_404(StudentProfile, pk=student_id, school=request.user.school)
    regenerate_link_code(student=student, created_by=request.user)
    messages.success(request, f'New link code issued for {student.full_name}.')
    return redirect('pages:school_admin_students')


@login_required
def parent_link_child(request):
    from accounts.forms_portal import ParentLinkCodeForm
    from students.link_service import link_parent_to_student

    if request.user.role != 'parent':
        return redirect('pages:dashboard')

    initial = {}
    if request.GET.get('code'):
        initial['code'] = request.GET.get('code').strip().upper()

    if request.method == 'POST':
        form = ParentLinkCodeForm(request.POST)
        if form.is_valid():
            try:
                _, created, student = link_parent_to_student(
                    parent_user=request.user,
                    code=form.cleaned_data['code'],
                    relationship=form.cleaned_data['relationship'],
                )
                if created:
                    messages.success(request, f'Linked to {student.full_name}.')
                else:
                    messages.info(request, f'Already linked to {student.full_name}.')
                return redirect('pages:dashboard_parent')
            except (PermissionError, ValueError) as exc:
                messages.error(request, str(exc))
    else:
        form = ParentLinkCodeForm(initial=initial)

    ctx = build_portal_context(
        request,
        'Link your child',
        'Enter the code your school gave you to connect your parent account.',
    )
    ctx['form'] = form
    return render(request, 'registration/parent_link_child.html', ctx)


def public_student_link(request, code):
    """Short link schools can share — sends parents to register or link flow."""
    from students.link_service import resolve_link_code

    row = resolve_link_code(code)
    if not row:
        messages.error(request, 'This link code is invalid or has expired.')
        return redirect('pages:register')

    if request.user.is_authenticated:
        if request.user.role == 'parent':
            return redirect(f'{reverse("pages:parent_link_child")}?code={row.code}')
        messages.warning(request, 'Log in as a parent account to use this link.')
        return redirect('pages:dashboard')

    return redirect(f'{reverse("pages:register")}?code={row.code}&school={row.school_id}')

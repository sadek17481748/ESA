"""messaging/views.py — portal messaging and support."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from pages.decorators import role_required
from pages.portal import build_portal_context
from parents.models import StudentParentLink
from teachers.models import TeacherProfile

from .forms import (
    NewSchoolMessageForm,
    SchoolReplyForm,
    SupportCaseForm,
    SupportReplyForm,
    TeacherReportForm,
)
from .models import SchoolConversation, SchoolMessage, SupportCase, SupportMessage, TeacherReport
from .services import (
    conversations_for_user,
    generate_case_number,
    support_cases_for_user,
    user_can_view_conversation,
)


def _message_ctx(request, title, meta):
    return build_portal_context(request, title, meta)


@login_required
def messages_inbox(request):
    """Unified inbox — support + school messages."""
    support = list(support_cases_for_user(request.user)[:20])
    school = list(conversations_for_user(request.user)[:30])
    ctx = _message_ctx(request, 'Messages', 'Support cases and school conversations.')
    ctx.update({
        'support_cases': support,
        'conversations': school,
        'can_support': request.user.role != 'super_admin',
    })
    return render(request, 'messaging/inbox.html', ctx)


@login_required
def support_new(request):
    if request.user.role == 'super_admin':
        return redirect('messaging:support_list')

    if request.method == 'POST':
        form = SupportCaseForm(request.POST)
        if form.is_valid():
            case = SupportCase.objects.create(
                case_number=generate_case_number(),
                opened_by=request.user,
                subject=form.cleaned_data['subject'],
            )
            SupportMessage.objects.create(
                case=case,
                sender=request.user,
                body=form.cleaned_data['message'],
            )
            messages.success(request, f'Support case {case.case_number} opened.')
            return redirect('messaging:support_detail', case_id=case.pk)
    else:
        form = SupportCaseForm()

    ctx = _message_ctx(request, 'Contact support', 'Open a case — our platform team will respond.')
    ctx['form'] = form
    return render(request, 'messaging/support_new.html', ctx)


@login_required
def support_list(request):
    return redirect('messaging:inbox')


@login_required
def support_detail(request, case_id):
    case = get_object_or_404(SupportCase, pk=case_id)
    if request.user.role != 'super_admin' and case.opened_by_id != request.user.pk:
        return redirect('messaging:inbox')

    if request.method == 'POST':
        form = SupportReplyForm(request.POST)
        if form.is_valid():
            is_staff = request.user.role == 'super_admin'
            SupportMessage.objects.create(
                case=case,
                sender=request.user,
                body=form.cleaned_data['message'],
                is_staff_reply=is_staff,
            )
            case.updated_at = timezone.now()
            if is_staff:
                case.status = SupportCase.STATUS_OPEN
            case.save(update_fields=['updated_at', 'status'])
            if request.POST.get('action') == 'close' and request.user.role == 'super_admin':
                case.status = SupportCase.STATUS_CLOSED
                case.save(update_fields=['status'])
            return redirect('messaging:support_detail', case_id=case.pk)
    else:
        form = SupportReplyForm()

    ctx = _message_ctx(request, case.case_number, case.subject)
    ctx.update({'case': case, 'form': form, 'thread': case.messages.select_related('sender')})
    return render(request, 'messaging/support_detail.html', ctx)


@login_required
def school_new(request):
    if request.user.role not in ('parent', 'teacher', 'school_admin'):
        return redirect('messaging:inbox')

    if request.method == 'POST':
        form = NewSchoolMessageForm(request.user, request.POST)
        if form.is_valid():
            kind = form.cleaned_data['recipient_kind']
            recipient_user = None
            recipient_type = SchoolConversation.RECIPIENT_SCHOOL
            if kind == 'teacher':
                recipient_type = SchoolConversation.RECIPIENT_TEACHER
                recipient_user = form.cleaned_data['teacher'].user
            elif kind == 'parent':
                recipient_type = SchoolConversation.RECIPIENT_PARENT
                recipient_user = form.cleaned_data['parent']

            conv = SchoolConversation.objects.create(
                school=request.user.school,
                subject=form.cleaned_data['subject'],
                created_by=request.user,
                recipient_type=recipient_type,
                recipient_user=recipient_user,
            )
            SchoolMessage.objects.create(
                conversation=conv,
                sender=request.user,
                body=form.cleaned_data['message'],
            )
            messages.success(request, 'Message sent.')
            return redirect('messaging:school_detail', conv_id=conv.pk)
    else:
        form = NewSchoolMessageForm(request.user)

    ctx = _message_ctx(request, 'New message', 'Message a teacher or your school office.')
    ctx['form'] = form
    return render(request, 'messaging/school_new.html', ctx)


@login_required
def school_detail(request, conv_id):
    conv = get_object_or_404(SchoolConversation, pk=conv_id)
    if not user_can_view_conversation(request.user, conv):
        return redirect('messaging:inbox')

    if request.method == 'POST':
        form = SchoolReplyForm(request.POST)
        if form.is_valid():
            SchoolMessage.objects.create(
                conversation=conv,
                sender=request.user,
                body=form.cleaned_data['message'],
            )
            conv.updated_at = timezone.now()
            conv.save(update_fields=['updated_at'])
            return redirect('messaging:school_detail', conv_id=conv.pk)
    else:
        form = SchoolReplyForm()

    ctx = _message_ctx(request, conv.subject, 'School conversation.')
    ctx.update({
        'conversation': conv,
        'thread': conv.messages.select_related('sender'),
        'form': form,
    })
    return render(request, 'messaging/school_detail.html', ctx)


@role_required('teacher')
def teacher_report_create(request):
    school = request.user.school
    if request.method == 'POST':
        form = TeacherReportForm(school, request.user, request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            parent_user = None
            if form.cleaned_data.get('send_to_parent'):
                link = StudentParentLink.objects.filter(student=student).select_related('parent__user').first()
                if link:
                    parent_user = link.parent.user
            TeacherReport.objects.create(
                school=school,
                teacher=request.user,
                student=student,
                parent=parent_user,
                subject_line=form.cleaned_data['subject_line'],
                period_covered=form.cleaned_data.get('period_covered', ''),
                strengths=form.cleaned_data.get('strengths', ''),
                areas_for_improvement=form.cleaned_data.get('areas_for_improvement', ''),
                action_required=form.cleaned_data.get('action_required', ''),
                additional_notes=form.cleaned_data.get('additional_notes', ''),
            )
            messages.success(request, f'Report sent for {student.full_name}.')
            return redirect('messaging:reports_list')
    else:
        form = TeacherReportForm(school, request.user)

    ctx = _message_ctx(
        request,
        'Create report',
        'Fill in the template and send to the student and linked parent.',
    )
    ctx['form'] = form
    return render(request, 'messaging/report_create.html', ctx)


@login_required
def reports_list(request):
    if request.user.role == 'teacher':
        reports = TeacherReport.objects.filter(teacher=request.user).select_related('student')
    elif request.user.role == 'parent':
        reports = TeacherReport.objects.filter(parent=request.user).select_related('student', 'teacher')
    elif request.user.role == 'student':
        from pages.enrollment_service import student_profile_for_user
        profile = student_profile_for_user(request.user)
        reports = TeacherReport.objects.filter(student=profile).select_related('teacher') if profile else []
    elif request.user.role == 'school_admin':
        reports = TeacherReport.objects.filter(school=request.user.school).select_related('student', 'teacher')
    else:
        reports = TeacherReport.objects.none()

    ctx = _message_ctx(request, 'Reports', 'Teacher progress reports.')
    ctx['reports'] = reports
    return render(request, 'messaging/reports_list.html', ctx)


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(TeacherReport, pk=report_id)
    user = request.user
    allowed = (
        report.teacher_id == user.pk
        or report.parent_id == user.pk
        or (user.role == 'student' and report.student.user_id and report.student.user_id == user.pk)
        or (user.role == 'school_admin' and report.school_id == user.school_id)
    )
    if not allowed:
        return redirect('messaging:reports_list')
    if user.pk in (report.parent_id, report.student.user_id) and not report.read_at:
        report.read_at = timezone.now()
        report.save(update_fields=['read_at'])

    ctx = _message_ctx(request, report.subject_line, report.period_covered)
    ctx['report'] = report
    return render(request, 'messaging/report_detail.html', ctx)

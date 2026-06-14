"""quran/views.py — Qur'an mushaf sessions with page notes and highlights."""
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from pages.decorators import role_required
from pages.enrollment_service import student_profile_for_user
from pages.portal import build_portal_context
from parents.models import StudentParentLink

from .forms import (
    QuranSessionForm,
    StudentAudioForm,
    TeacherFeedbackAudioForm,
)
from .models import QuranSession
from .mushaf import MUSHAF_PARA_COUNT, para_pdf_url
from .services import get_page_markup, mark_session_reviewed, save_page_markup


def _ctx(request, title, meta=''):
    return build_portal_context(request, title, meta)


def _sessions_for_user(user):
    if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
        return QuranSession.objects.filter(
            teacher=user.teacher_profile,
        ).select_related('student', 'teacher')
    if user.role == 'student' and hasattr(user, 'student_profile'):
        return QuranSession.objects.filter(
            student=user.student_profile,
        ).select_related('student', 'teacher')
    if user.role == 'parent' and hasattr(user, 'parent_profile'):
        child_ids = StudentParentLink.objects.filter(
            parent=user.parent_profile,
        ).values_list('student_id', flat=True)
        return QuranSession.objects.filter(
            student_id__in=child_ids,
        ).select_related('student', 'teacher')
    if user.role == 'school_admin' and user.school_id:
        return QuranSession.objects.filter(
            school=user.school,
        ).select_related('student', 'teacher')
    return QuranSession.objects.none()


def _session_allowed(user, session):
    if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
        return session.teacher_id == user.teacher_profile.id
    if user.role == 'student' and hasattr(user, 'student_profile'):
        return session.student_id == user.student_profile.id
    if user.role == 'parent' and hasattr(user, 'parent_profile'):
        return StudentParentLink.objects.filter(
            parent=user.parent_profile, student=session.student,
        ).exists()
    if user.role == 'school_admin':
        return session.school_id == user.school_id
    return False


def _parse_page_params(request):
    try:
        para = int(request.GET.get('para', 1))
    except (TypeError, ValueError):
        para = 1
    try:
        page = int(request.GET.get('page', 1))
    except (TypeError, ValueError):
        page = 1
    para = max(1, min(MUSHAF_PARA_COUNT, para))
    page = max(1, page)
    return para, page


@login_required
def quran_list(request):
    sessions = _sessions_for_user(request.user)
    ctx = _ctx(
        request,
        'Qur’an sessions',
        'Open the mushaf, add page notes, and highlight like a word processor.',
    )
    ctx['sessions'] = sessions
    ctx['can_create'] = request.user.role == 'teacher'
    return render(request, 'quran/list.html', ctx)


@role_required('teacher')
def quran_create_session(request):
    teacher = request.user.teacher_profile
    if request.method == 'POST':
        form = QuranSessionForm(request.user.school, request.POST)
        if form.is_valid():
            session = form.save(school=request.user.school, teacher=teacher)
            messages.success(request, f'Session created for {session.student.full_name}.')
            return redirect('quran:session_detail', session_id=session.pk)
    else:
        form = QuranSessionForm(request.user.school)
    ctx = _ctx(request, 'New Qur’an session', 'Pick a student — then turn pages in the mushaf.')
    ctx['form'] = form
    return render(request, 'quran/session_form.html', ctx)


@login_required
def quran_session_detail(request, session_id):
    session = get_object_or_404(
        QuranSession.objects.select_related('student', 'teacher'),
        pk=session_id,
    )
    if not _session_allowed(request.user, session):
        return redirect('pages:dashboard')

    para, page = _parse_page_params(request)
    markup = get_page_markup(session, para, page)

    is_teacher = (
        request.user.role == 'teacher'
        and hasattr(request.user, 'teacher_profile')
        and session.teacher_id == request.user.teacher_profile.id
    )
    is_student = (
        request.user.role == 'student'
        and hasattr(request.user, 'student_profile')
        and session.student_id == request.user.student_profile.id
    )

    audio_form = StudentAudioForm() if is_student else None
    feedback_form = TeacherFeedbackAudioForm() if is_teacher else None

    ctx = _ctx(
        request,
        session.display_title,
        f'Juz {para} · page {page} — notes and highlights save for this student only.',
    )
    ctx.update({
        'session': session,
        'para_number': para,
        'page_number': page,
        'para_count': MUSHAF_PARA_COUNT,
        'pdf_url': para_pdf_url(para),
        'page_note': markup.note if markup else '',
        'page_highlights_json': json.dumps(markup.highlights if markup else []),
        'can_edit': is_teacher,
        'audio_form': audio_form,
        'feedback_form': feedback_form,
        'is_teacher': is_teacher,
        'is_student': is_student,
    })
    return render(request, 'quran/session_detail.html', ctx)


@login_required
@require_GET
def quran_page_data(request, session_id):
    session = get_object_or_404(QuranSession, pk=session_id)
    if not _session_allowed(request.user, session):
        return JsonResponse({'error': 'Not allowed'}, status=403)
    para, page = _parse_page_params(request)
    markup = get_page_markup(session, para, page)
    return JsonResponse({
        'para_number': para,
        'page_number': page,
        'note': markup.note if markup else '',
        'highlights': markup.highlights if markup else [],
    })


@role_required('teacher')
@require_POST
def quran_save_page(request, session_id):
    session = get_object_or_404(QuranSession, pk=session_id, teacher=request.user.teacher_profile)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:
        para = int(payload.get('para_number', 1))
        page = int(payload.get('page_number', 1))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid page'}, status=400)

    para = max(1, min(MUSHAF_PARA_COUNT, para))
    page = max(1, page)

    save_page_markup(
        session=session,
        para_number=para,
        page_number=page,
        note=(payload.get('note') or '')[:5000],
        highlights=payload.get('highlights', []),
    )
    return JsonResponse({'ok': True})


@login_required
@require_POST
def quran_upload_audio(request, session_id):
    profile = student_profile_for_user(request.user)
    session = get_object_or_404(QuranSession, pk=session_id, student=profile)
    form = StudentAudioForm(request.POST, request.FILES)
    if form.is_valid():
        session.student_audio = form.cleaned_data['student_audio']
        session.status = QuranSession.STATUS_SUBMITTED
        session.save(update_fields=['student_audio', 'status', 'updated_at'])
        messages.success(request, 'Recitation uploaded.')
    else:
        messages.error(request, 'Please choose an audio file.')
    return redirect('quran:session_detail', session_id=session.pk)


@role_required('teacher')
@require_POST
def quran_upload_feedback(request, session_id):
    session = get_object_or_404(QuranSession, pk=session_id, teacher=request.user.teacher_profile)
    form = TeacherFeedbackAudioForm(request.POST, request.FILES)
    if form.is_valid():
        if form.cleaned_data.get('teacher_feedback_audio'):
            session.teacher_feedback_audio = form.cleaned_data['teacher_feedback_audio']
        session.teacher_notes = form.cleaned_data.get('teacher_notes', session.teacher_notes)
        session.save(update_fields=['teacher_feedback_audio', 'teacher_notes', 'updated_at'])
        try:
            mark_session_reviewed(
                session, request.user.teacher_profile, notes=session.teacher_notes,
            )
        except PermissionError as exc:
            messages.error(request, str(exc))
            return redirect('quran:session_detail', session_id=session.pk)
        messages.success(request, 'Feedback saved and session marked reviewed.')
    else:
        messages.error(request, 'Could not save feedback.')
    return redirect('quran:session_detail', session_id=session.pk)

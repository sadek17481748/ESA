"""quran/views.py — Qur'an recitation sessions and annotations."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pages.decorators import role_required
from pages.enrollment_service import student_profile_for_user
from pages.portal import build_portal_context
from parents.models import StudentParentLink

from .forms import (
    QuranAnnotationForm,
    QuranSessionForm,
    StudentAudioForm,
    TeacherFeedbackAudioForm,
)
from .models import QuranSession
from .services import add_annotation, mark_session_reviewed


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


@login_required
def quran_list(request):
    sessions = _sessions_for_user(request.user)
    ctx = _ctx(
        request,
        'Qur’an annotation',
        'Ayah display, mistake tags, timestamps, and audio feedback.',
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
    ctx = _ctx(request, 'New recitation session', 'Select student and ayah range.')
    ctx['form'] = form
    return render(request, 'quran/session_form.html', ctx)


@login_required
def quran_session_detail(request, session_id):
    session = get_object_or_404(
        QuranSession.objects.select_related('student', 'teacher').prefetch_related('annotations'),
        pk=session_id,
    )
    user = request.user
    allowed = False
    if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
        allowed = session.teacher_id == user.teacher_profile.id
    elif user.role == 'student' and hasattr(user, 'student_profile'):
        allowed = session.student_id == user.student_profile.id
    elif user.role == 'parent' and hasattr(user, 'parent_profile'):
        allowed = StudentParentLink.objects.filter(
            parent=user.parent_profile, student=session.student,
        ).exists()
    elif user.role == 'school_admin':
        allowed = session.school_id == user.school_id
    if not allowed:
        return redirect('pages:dashboard')

    annotation_form = None
    audio_form = None
    feedback_form = None
    is_teacher = user.role == 'teacher' and session.teacher_id == user.teacher_profile.id
    is_student = user.role == 'student' and session.student_id == user.student_profile.id

    if is_teacher:
        annotation_form = QuranAnnotationForm()
        feedback_form = TeacherFeedbackAudioForm()
    if is_student:
        audio_form = StudentAudioForm()

    ctx = _ctx(request, f'{session.surah_name}', session.ayah_text[:80])
    ctx.update({
        'session': session,
        'annotations': session.annotations.all(),
        'annotation_form': annotation_form,
        'audio_form': audio_form,
        'feedback_form': feedback_form,
        'is_teacher': is_teacher,
        'is_student': is_student,
    })
    return render(request, 'quran/session_detail.html', ctx)


@role_required('teacher')
@require_POST
def quran_add_annotation(request, session_id):
    session = get_object_or_404(QuranSession, pk=session_id, teacher=request.user.teacher_profile)
    form = QuranAnnotationForm(request.POST)
    if form.is_valid():
        try:
            add_annotation(
                session=session,
                teacher_profile=request.user.teacher_profile,
                ayah_number=form.cleaned_data['ayah_number'],
                tag=form.cleaned_data['tag'],
                timestamp_seconds=form.cleaned_data['timestamp_seconds'],
                comment=form.cleaned_data.get('comment', ''),
            )
            messages.success(request, 'Annotation added.')
        except PermissionError as exc:
            messages.error(request, str(exc))
    else:
        messages.error(request, 'Could not save annotation — check the form.')
    return redirect('quran:session_detail', session_id=session.pk)


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

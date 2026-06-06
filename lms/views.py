"""lms/views.py — school LMS portal."""
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from pages.decorators import role_required
from pages.enrollment_service import student_class_group, student_profile_for_user
from pages.portal import build_portal_context

from .forms import AssignTrackForm, CourseMaterialForm, CourseSubjectForm, CourseTrackForm, MaterialSubmissionForm
from .models import (
    ClassTrackAssignment,
    CourseMaterial,
    CourseSubject,
    CourseTrack,
    MaterialSubmission,
    StudentMaterialProgress,
)
from .services import mark_material_progress, materials_for_student, student_track_summaries, tracks_for_class


def _ctx(request, title, meta):
    return build_portal_context(request, title, meta)


@role_required('school_admin')
def lms_hub(request):
    school = request.user.school
    subjects = CourseSubject.objects.filter(school=school).prefetch_related('tracks', 'tracks__materials')
    ctx = _ctx(request, 'LMS', 'Create subjects, upload content, and manage learning materials.')
    ctx['subjects'] = subjects
    return render(request, 'lms/hub.html', ctx)


@role_required('school_admin')
def lms_subject_create(request):
    school = request.user.school
    if request.method == 'POST':
        form = CourseSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.school = school
            subject.save()
            messages.success(request, f'Created subject {subject.name}.')
            return redirect('lms:hub')
    else:
        form = CourseSubjectForm()
    ctx = _ctx(request, 'New subject', 'Add a subject to your school LMS.')
    ctx['form'] = form
    return render(request, 'lms/subject_form.html', ctx)


@role_required('school_admin')
def lms_track_create(request, subject_id):
    subject = get_object_or_404(CourseSubject, pk=subject_id, school=request.user.school)
    if request.method == 'POST':
        form = CourseTrackForm(request.POST)
        if form.is_valid():
            track = form.save(commit=False)
            track.subject = subject
            track.save()
            messages.success(request, f'Created track {track.name}.')
            return redirect('lms:hub')
    else:
        form = CourseTrackForm()
    ctx = _ctx(request, f'New track — {subject.name}', 'e.g. Foundation, Higher, GCSE.')
    ctx.update({'form': form, 'subject': subject})
    return render(request, 'lms/track_form.html', ctx)


@role_required('school_admin')
def lms_material_upload(request, track_id):
    track = get_object_or_404(CourseTrack, pk=track_id, subject__school=request.user.school)
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.track = track
            material.save()
            messages.success(request, f'Uploaded {material.title}.')
            return redirect('lms:hub')
    else:
        form = CourseMaterialForm()
    ctx = _ctx(request, f'Upload — {track}', 'Worksheets, documents, videos, or links.')
    ctx.update({'form': form, 'track': track})
    return render(request, 'lms/material_form.html', ctx)


@role_required('teacher', 'school_admin')
def lms_assign(request):
    school = request.user.school
    if request.method == 'POST':
        form = AssignTrackForm(school, request.POST)
        if form.is_valid():
            ClassTrackAssignment.objects.get_or_create(
                class_group=form.cleaned_data['class_group'],
                track=form.cleaned_data['track'],
                defaults={'assigned_by': request.user},
            )
            messages.success(request, 'Track assigned to class.')
            return redirect('lms:assign')
    else:
        form = AssignTrackForm(school)

    assignments = ClassTrackAssignment.objects.filter(
        track__subject__school=school,
    ).select_related('class_group', 'track', 'track__subject')

    ctx = _ctx(request, 'Assign content', 'Assign a subject level to a class you teach.')
    ctx.update({'form': form, 'assignments': assignments})
    return render(request, 'lms/assign.html', ctx)


@login_required
def lms_student_worksheets(request):
    """Student/parent view of assigned LMS content with progress."""
    if request.user.role == 'student':
        profile = student_profile_for_user(request.user)
        if not profile:
            return redirect('pages:dashboard')
        summaries = student_track_summaries(profile)
        materials = list(materials_for_student(profile))
        progress_map = {
            p.material_id: p.progress_percent
            for p in StudentMaterialProgress.objects.filter(student=profile)
        }
        submission_map = {
            s.material_id: s
            for s in MaterialSubmission.objects.filter(student=profile)
        }
        materials_with_progress = [
            {
                'material': m,
                'progress': progress_map.get(m.pk, 0),
                'submission': submission_map.get(m.pk),
            }
            for m in materials
        ]
        ctx = _ctx(request, 'My learning', 'Subjects and assignments for your class.')
        ctx.update({
            'summaries': summaries,
            'materials_with_progress': materials_with_progress,
            'student': profile,
        })
        return render(request, 'lms/student_worksheets.html', ctx)

    if request.user.role == 'teacher':
        from teachers.models import TeacherProfile
        from academics.models import ClassGroup
        profile = TeacherProfile.objects.filter(user=request.user).first()
        classes = ClassGroup.objects.filter(school=request.user.school, teacher=profile) if profile else []
        pending = MaterialSubmission.objects.filter(
            material__track__subject__school=request.user.school,
            status=MaterialSubmission.STATUS_PENDING,
        ).select_related('student', 'material', 'material__track')
        ctx = _ctx(request, 'Class content', 'View and assign LMS materials to your classes.')
        ctx.update({
            'classes': classes,
            'assign_url': 'lms:assign',
            'pending_submissions': pending,
        })
        return render(request, 'lms/teacher_worksheets.html', ctx)

    if request.user.role == 'school_admin':
        return redirect('lms:hub')

    return redirect('pages:dashboard')


@login_required
@require_POST
def lms_mark_complete(request, material_id):
    if request.user.role != 'student':
        return redirect('pages:worksheets')
    profile = student_profile_for_user(request.user)
    material = get_object_or_404(CourseMaterial, pk=material_id)
    mark_material_progress(profile, material, status=StudentMaterialProgress.STATUS_COMPLETED, progress_percent=100)
    messages.success(request, f'Marked {material.title} as complete.')
    return redirect('pages:worksheets')


@login_required
@require_POST
def lms_submit_material(request, material_id):
    if request.user.role != 'student':
        return redirect('pages:worksheets')
    profile = student_profile_for_user(request.user)
    material = get_object_or_404(CourseMaterial, pk=material_id)
    form = MaterialSubmissionForm(request.POST, request.FILES)
    if form.is_valid():
        submission, _ = MaterialSubmission.objects.get_or_create(
            student=profile,
            material=material,
        )
        submission.file = form.cleaned_data['file']
        submission.notes = form.cleaned_data.get('notes', '')
        submission.status = MaterialSubmission.STATUS_PENDING
        submission.save()
        mark_material_progress(
            profile, material,
            status=StudentMaterialProgress.STATUS_IN_PROGRESS,
            progress_percent=50,
        )
        messages.success(request, f'Submitted {material.title} for review.')
    else:
        messages.error(request, 'Please choose a file to upload.')
    return redirect('pages:worksheets')


@role_required('teacher')
@require_POST
def lms_review_submission(request, submission_id):
    submission = get_object_or_404(
        MaterialSubmission,
        pk=submission_id,
        material__track__subject__school=request.user.school,
    )
    action = request.POST.get('action')
    feedback = request.POST.get('feedback', '')
    if action == 'approve':
        submission.status = MaterialSubmission.STATUS_APPROVED
        mark_material_progress(
            submission.student,
            submission.material,
            status=StudentMaterialProgress.STATUS_COMPLETED,
            progress_percent=100,
        )
    elif action == 'reject':
        submission.status = MaterialSubmission.STATUS_REJECTED
    submission.teacher_feedback = feedback
    submission.reviewed_by = request.user
    submission.reviewed_at = timezone.now()
    submission.save()
    messages.success(request, 'Submission reviewed.')
    return redirect('pages:worksheets')

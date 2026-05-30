"""lms/services.py — LMS progress and class content helpers."""
from django.db.models import Avg, Count, Q
from django.utils import timezone

from academics.models import ClassEnrollment

from .models import ClassTrackAssignment, CourseMaterial, StudentMaterialProgress


def tracks_for_class(class_group):
    return ClassTrackAssignment.objects.filter(
        class_group=class_group,
    ).select_related('track', 'track__subject', 'assigned_by')


def materials_for_student(student):
    """All materials from tracks assigned to the student's class(es)."""
    class_ids = ClassEnrollment.objects.filter(student=student).values_list('class_group_id', flat=True)
    track_ids = ClassTrackAssignment.objects.filter(
        class_group_id__in=class_ids,
    ).values_list('track_id', flat=True)
    return CourseMaterial.objects.filter(track_id__in=track_ids).select_related(
        'track', 'track__subject',
    ).order_by('track__subject__name', 'track__sort_order', 'sort_order')


def track_progress(student, track):
    materials = CourseMaterial.objects.filter(track=track)
    total = materials.count()
    if not total:
        return 0, 0, 0
    progress = StudentMaterialProgress.objects.filter(student=student, material__in=materials)
    completed = progress.filter(status=StudentMaterialProgress.STATUS_COMPLETED).count()
    avg = progress.aggregate(avg=Avg('progress_percent'))['avg'] or 0
    return completed, total, int(avg)


def student_track_summaries(student):
    class_ids = ClassEnrollment.objects.filter(student=student).values_list('class_group_id', flat=True)
    assignments = ClassTrackAssignment.objects.filter(
        class_group_id__in=class_ids,
    ).select_related('track', 'track__subject')
    summaries = []
    for assignment in assignments:
        completed, total, avg = track_progress(student, assignment.track)
        summaries.append({
            'assignment': assignment,
            'track': assignment.track,
            'subject': assignment.track.subject,
            'completed': completed,
            'total': total,
            'progress_percent': int((completed / total) * 100) if total else 0,
        })
    return summaries


def mark_material_progress(student, material, *, status=None, progress_percent=None):
    prog, _ = StudentMaterialProgress.objects.get_or_create(
        student=student,
        material=material,
    )
    if status:
        prog.status = status
    if progress_percent is not None:
        prog.progress_percent = min(100, max(0, progress_percent))
    if prog.status == StudentMaterialProgress.STATUS_COMPLETED or prog.progress_percent >= 100:
        prog.status = StudentMaterialProgress.STATUS_COMPLETED
        prog.progress_percent = 100
        if not prog.completed_at:
            prog.completed_at = timezone.now()
    elif prog.progress_percent > 0:
        prog.status = StudentMaterialProgress.STATUS_IN_PROGRESS
    prog.save()
    return prog

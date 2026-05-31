"""
homework/services.py
Teacher sign-off — only assigned teacher can approve/reject.
"""
from django.utils import timezone

from notifications.services import notify_user

from .models import Submission


def sign_off_submission(*, submission, teacher_profile, approve, note=''):
    assignment = submission.assignment
    if assignment.teacher_id != teacher_profile.id:
        raise PermissionError('Only the assigning teacher can sign off this submission.')
    if submission.status not in (Submission.STATUS_SUBMITTED, Submission.STATUS_DRAFT):
        raise ValueError('Submission is not awaiting sign-off.')

    submission.status = Submission.STATUS_APPROVED if approve else Submission.STATUS_REJECTED
    submission.teacher_note = note
    submission.signed_off_by = teacher_profile
    submission.signed_off_at = timezone.now()
    submission.save(update_fields=['status', 'teacher_note', 'signed_off_by', 'signed_off_at'])

    if submission.student.user_id:
        notify_user(
            user=submission.student.user,
            school=assignment.school,
            notification_type='signoff',
            title='Work signed off' if approve else 'Work needs revision',
            message=f'{assignment.title}: {"approved" if approve else "rejected"}',
            link_path=f'/homework/submissions/{submission.pk}/',
        )
    return submission


def sign_off_submission(*, submission, teacher_profile, approve, note=''):
    submission.status = Submission.STATUS_APPROVED if approve else Submission.STATUS_REJECTED
    submission.save()
    return submission

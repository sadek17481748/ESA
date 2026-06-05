"""Parent dashboard — children summary with attendance and LMS progress."""
from datetime import timedelta

from lms.services import student_track_summaries
from pages.attendance_service import parent_children_attendance, session_date_or_today


def parent_children_summary(parent_user, session_date=None):
    """Extend attendance children rows with homework progress this week."""
    session_date = session_date_or_today(session_date)
    week_start = session_date - timedelta(days=session_date.weekday())
    children = parent_children_attendance(parent_user, session_date)

    for child_row in children:
        student = child_row['student']
        summaries = student_track_summaries(student)
        total_materials = sum(s['total'] for s in summaries)
        completed = sum(s['completed'] for s in summaries)
        child_row['lms_completed'] = completed
        child_row['lms_total'] = total_materials
        child_row['lms_percent'] = int((completed / total_materials) * 100) if total_materials else 0
        child_row['lms_subjects'] = summaries

        week_marks = [
            m for m in child_row.get('history', [])
            if m.session.session_date >= week_start
        ]
        present = sum(1 for m in week_marks if m.status == 'present')
        child_row['week_present'] = present
        child_row['week_total'] = len(week_marks)

    return children

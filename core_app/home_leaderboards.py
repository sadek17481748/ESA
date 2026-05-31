"""
core_app/home_leaderboards.py
Weekly leaderboard data for the public homepage.
"""
from datetime import timedelta

from django.db.models import Count, F, Q
from django.utils import timezone

from schools.models import School
from students.models import StudentProfile


def _week_start():
    return timezone.now() - timedelta(days=7)


def get_students_of_the_week(limit=10):
    """
    Rank students by activity in the last 7 days:
    homework submitted/approved (3 pts each) + present/late attendance (1 pt each).
    """
    since = _week_start()
    since_date = since.date()

    rows = (
        StudentProfile.objects.filter(is_active=True)
        .select_related('school')
        .annotate(
            homework_pts=Count(
                'submissions',
                filter=Q(
                    submissions__submitted_at__gte=since,
                    submissions__status__in=('submitted', 'approved'),
                ),
                distinct=True,
            ),
            attendance_pts=Count(
                'attendance_marks',
                filter=Q(
                    attendance_marks__session__session_date__gte=since_date,
                    attendance_marks__status__in=('present', 'late'),
                ),
                distinct=True,
            ),
        )
        .annotate(week_score=F('homework_pts') * 3 + F('attendance_pts'))
        .order_by('-week_score', 'last_name', 'first_name')[:limit]
    )

    return [
        {
            'rank': i + 1,
            'name': f'{s.first_name} {s.last_name}'.strip(),
            'school': s.school.name,
            'year_group': s.year_group or '—',
            'score': s.week_score,
            'homework': s.homework_pts,
            'attendance': s.attendance_pts,
        }
        for i, s in enumerate(rows)
    ]


def get_schools_of_the_week(limit=10):
    """
    Rank schools by platform activity in the last 7 days:
    new user sign-ups (5 pts) + attendance sessions (2 pts) + active student count.
    """
    since = _week_start()
    since_date = since.date()

    rows = (
        School.objects.filter(status=School.STATUS_ACTIVE)
        .annotate(
            new_users=Count(
                'users',
                filter=Q(users__date_joined__gte=since),
                distinct=True,
            ),
            weekly_sessions=Count(
                'attendance_sessions',
                filter=Q(attendance_sessions__session_date__gte=since_date),
                distinct=True,
            ),
            student_total=Count('students', distinct=True),
        )
        .annotate(
            week_score=F('new_users') * 5 + F('weekly_sessions') * 2 + F('student_total'),
        )
        .order_by('-week_score', 'name')[:limit]
    )

    return [
        {
            'rank': i + 1,
            'name': s.name,
            'tier': s.get_subscription_tier_display(),
            'tier_key': s.subscription_tier,
            'students': s.student_total,
            'new_users': s.new_users,
            'sessions': s.weekly_sessions,
            'score': s.week_score,
        }
        for i, s in enumerate(rows)
    ]

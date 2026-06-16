"""
core_app/home_leaderboards.py
Weekly leaderboard data for the public homepage.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, F, IntegerField, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone

from attendance.models import AttendanceMark, AttendanceSession
from homework.models import Submission
from schools.models import School
from students.models import StudentProfile

User = get_user_model()


def _week_start():
    return timezone.now() - timedelta(days=7)


def get_students_of_the_week(limit=10):
    """
    Rank students by activity in the last 7 days:
    homework submitted/approved (3 pts each) + present/late attendance (1 pt each).
    """
    since = _week_start()
    since_date = since.date()

    homework_sq = (
        Submission.objects.filter(
            student_id=OuterRef('pk'),
            submitted_at__gte=since,
            status__in=(Submission.STATUS_SUBMITTED, Submission.STATUS_APPROVED),
        )
        .values('student_id')
        .annotate(c=Count('id'))
        .values('c')[:1]
    )
    attendance_sq = (
        AttendanceMark.objects.filter(
            student_id=OuterRef('pk'),
            session__session_date__gte=since_date,
            status__in=('present', 'late'),
        )
        .values('student_id')
        .annotate(c=Count('id'))
        .values('c')[:1]
    )

    rows = (
        StudentProfile.objects.filter(is_active=True)
        .select_related('school')
        .annotate(
            homework_pts=Coalesce(Subquery(homework_sq, output_field=IntegerField()), 0),
            attendance_pts=Coalesce(Subquery(attendance_sq, output_field=IntegerField()), 0),
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

    # Separate subqueries avoid a multi-join Count explosion on large tenants.
    new_users_sq = (
        User.objects.filter(school_id=OuterRef('pk'), date_joined__gte=since)
        .values('school_id')
        .annotate(c=Count('id'))
        .values('c')[:1]
    )
    weekly_sessions_sq = (
        AttendanceSession.objects.filter(
            school_id=OuterRef('pk'),
            session_date__gte=since_date,
        )
        .values('school_id')
        .annotate(c=Count('id'))
        .values('c')[:1]
    )
    student_total_sq = (
        StudentProfile.objects.filter(school_id=OuterRef('pk'))
        .values('school_id')
        .annotate(c=Count('id'))
        .values('c')[:1]
    )

    rows = (
        School.objects.filter(status=School.STATUS_ACTIVE)
        .annotate(
            new_users=Coalesce(Subquery(new_users_sq, output_field=IntegerField()), 0),
            weekly_sessions=Coalesce(Subquery(weekly_sessions_sq, output_field=IntegerField()), 0),
            student_total=Coalesce(Subquery(student_total_sq, output_field=IntegerField()), 0),
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

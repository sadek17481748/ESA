"""
pages/super_admin_stats.py
Aggregates platform-wide metrics for the super admin dashboard.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.utils import timezone

from audit.models import AuditLog
from parents.models import ParentProfile
from payments.models import Payment
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()

TIER_MONTHLY_PENCE = {
    School.TIER_FREE: 0,
    School.TIER_STANDARD: 4900,
    School.TIER_PREMIUM: 9900,
}

TIER_LABELS = dict(School.TIER_CHOICES)


def _format_gbp(pence):
    return f'£{pence / 100:,.2f}'


def build_super_admin_dashboard_context():
    now = timezone.now()
    live_cutoff = now - timedelta(minutes=30)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    schools_qs = School.objects.annotate(
        user_count=Count('users', distinct=True),
        student_count=Count('students', distinct=True),
        teacher_count=Count('teachers', distinct=True),
        parent_count=Count('parents', distinct=True),
    ).order_by('-created_at')

    schools = list(schools_qs)
    tier_counts = {tier: 0 for tier, _ in School.TIER_CHOICES}
    status_counts = {status: 0 for status, _ in School.STATUS_CHOICES}
    mrr_pence = 0

    for school in schools:
        tier_counts[school.subscription_tier] = tier_counts.get(school.subscription_tier, 0) + 1
        status_counts[school.status] = status_counts.get(school.status, 0) + 1
        if school.status == School.STATUS_ACTIVE:
            mrr_pence += TIER_MONTHLY_PENCE.get(school.subscription_tier, 0)

    users_by_role = (
        User.objects.values('role')
        .annotate(count=Count('id'))
        .order_by('role')
    )
    role_totals = {row['role']: row['count'] for row in users_by_role}

    live_users = User.objects.filter(last_login__gte=live_cutoff).count()
    recent_logins = (
        AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN, created_at__gte=live_cutoff)
        .values('user_id')
        .distinct()
        .count()
    )
    active_now = max(live_users, recent_logins)

    payment_totals = Payment.objects.filter(status=Payment.STATUS_COMPLETE).aggregate(
        total_pence=Sum('amount_pence'),
        payment_count=Count('id'),
    )

    recent_users = (
        User.objects.select_related('school')
        .order_by('-date_joined')[:10]
    )
    recent_audit = (
        AuditLog.objects.select_related('user', 'school')
        .order_by('-created_at')[:15]
    )

    subscription_rows = []
    for tier, _ in School.TIER_CHOICES:
        count = tier_counts.get(tier, 0)
        subscription_rows.append({
            'tier': tier,
            'label': TIER_LABELS[tier],
            'school_count': count,
            'monthly_pence': TIER_MONTHLY_PENCE[tier],
            'monthly_display': _format_gbp(TIER_MONTHLY_PENCE[tier]),
            'mrr_contribution_pence': count * TIER_MONTHLY_PENCE[tier],
            'mrr_contribution_display': _format_gbp(count * TIER_MONTHLY_PENCE[tier]),
        })

    return {
        'generated_at': now,
        'kpis': {
            'schools_total': len(schools),
            'schools_active': status_counts.get(School.STATUS_ACTIVE, 0),
            'schools_suspended': status_counts.get(School.STATUS_SUSPENDED, 0),
            'users_total': User.objects.count(),
            'students_total': StudentProfile.objects.count(),
            'teachers_total': TeacherProfile.objects.count(),
            'parents_total': ParentProfile.objects.count(),
            'active_now': active_now,
            'new_users_7d': User.objects.filter(date_joined__gte=week_ago).count(),
            'new_schools_30d': School.objects.filter(created_at__gte=month_ago).count(),
            'mrr_display': _format_gbp(mrr_pence),
            'payments_total_display': _format_gbp(payment_totals['total_pence'] or 0),
            'payments_count': payment_totals['payment_count'] or 0,
        },
        'role_totals': role_totals,
        'subscription_rows': subscription_rows,
        'schools': schools,
        'recent_users': recent_users,
        'recent_audit': recent_audit,
        'live_cutoff_minutes': 30,
    }

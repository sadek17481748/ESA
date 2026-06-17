"""
pages/super_admin_stats.py
Aggregates platform-wide metrics for the super admin dashboard.
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from audit.models import AuditLog
from parents.models import ParentProfile
from payments.models import Payment, SubscriptionPayment
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


def _count_subquery(model, fk_field='school_id'):
    """Correlated subquery — avoids multi-join Count explosions on Heroku Postgres."""
    return (
        model.objects.filter(**{fk_field: OuterRef('pk')})
        .values(fk_field)
        .annotate(c=Count('id'))
        .values('c')[:1]
    )


def build_super_admin_dashboard_context():
    now = timezone.now()
    live_cutoff = now - timedelta(minutes=30)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    schools_qs = (
        School.objects.annotate(
            user_count=Coalesce(
                Subquery(_count_subquery(User), output_field=IntegerField()), 0,
            ),
            student_count=Coalesce(
                Subquery(_count_subquery(StudentProfile), output_field=IntegerField()), 0,
            ),
            teacher_count=Coalesce(
                Subquery(_count_subquery(TeacherProfile), output_field=IntegerField()), 0,
            ),
            parent_count=Coalesce(
                Subquery(_count_subquery(ParentProfile), output_field=IntegerField()), 0,
            ),
        )
        .order_by('-created_at')
    )

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

    subscription_payments = list(
        SubscriptionPayment.objects.select_related('school', 'admin')
        .order_by('-created_at')[:100]
    )

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
        'subscription_payments': subscription_payments,
        'schools': schools,
        'recent_users': recent_users,
        'recent_audit': recent_audit,
        'live_cutoff_minutes': 30,
    }

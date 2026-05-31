"""payments/school_fees.py — helpers for school admin fee overview."""
from django.db.models import Count, Q

from parents.models import StudentParentLink
from students.models import StudentProfile

from .models import FeeItem


def build_school_fee_overview(school):
    """Rows for each student with parent and latest fee status."""
    students = (
        StudentProfile.objects.filter(school=school, is_active=True)
        .order_by('last_name', 'first_name')
    )
    fees = FeeItem.objects.filter(school=school).select_related('parent')
    fees_by_child = {}
    for fee in fees:
        fees_by_child.setdefault(fee.child_name, []).append(fee)

    rows = []
    for student in students:
        child_name = f'{student.first_name} {student.last_name}'.strip()
        link = StudentParentLink.objects.filter(student=student).select_related(
            'parent__user',
        ).first()
        parent_user = link.parent.user if link else None
        student_fees = fees_by_child.get(child_name, [])
        latest = max(student_fees, key=lambda f: f.due_date, default=None) if student_fees else None
        rows.append({
            'student': student,
            'child_name': child_name,
            'parent_username': parent_user.username if parent_user else '—',
            'parent_name': parent_user.get_full_name() if parent_user else '—',
            'fees': student_fees,
            'latest_fee': latest,
            'status': latest.get_status_display() if latest else 'No fee set',
            'status_code': latest.status if latest else 'none',
        })

    totals = FeeItem.objects.filter(school=school).aggregate(
        total=Count('id'),
        paid=Count('id', filter=Q(status=FeeItem.STATUS_PAID)),
        outstanding=Count('id', filter=Q(status=FeeItem.STATUS_OUTSTANDING)),
        overdue=Count('id', filter=Q(status=FeeItem.STATUS_OVERDUE)),
    )
    return rows, totals


def create_fees_for_students(school, *, title, amount_pence, due_date, student=None):
    """Create fee items for one student or every student with a linked parent."""
    students = [student] if student else StudentProfile.objects.filter(
        school=school, is_active=True,
    )
    created = []
    for profile in students:
        link = StudentParentLink.objects.filter(student=profile).select_related('parent__user').first()
        if not link:
            continue
        child_name = f'{profile.first_name} {profile.last_name}'.strip()
        fee = FeeItem.objects.create(
            school=school,
            parent=link.parent.user,
            child_name=child_name,
            title=title,
            amount_pence=amount_pence,
            due_date=due_date,
        )
        created.append(fee)
    return created

"""School admin analytics — lightweight KPIs."""
from academics.models import ClassEnrollment
from attendance.models import AttendanceMark, AttendanceSession
from pages.attendance_service import session_date_or_today
from payments.models import FeeItem
from students.models import StudentProfile


def school_analytics(school, session_date=None):
    session_date = session_date_or_today(session_date)

    student_count = StudentProfile.objects.filter(school=school, is_active=True).count()
    enrolled = ClassEnrollment.objects.filter(class_group__school=school).values('student_id').distinct().count()

    fees = FeeItem.objects.filter(school=school)
    fee_totals = {
        'outstanding_pence': sum(
            f.amount_pence for f in fees.filter(status=FeeItem.STATUS_OUTSTANDING)
        ),
        'overdue_pence': sum(
            f.amount_pence for f in fees.filter(status=FeeItem.STATUS_OVERDUE)
        ),
        'paid_count': fees.filter(status=FeeItem.STATUS_PAID).count(),
        'outstanding_count': fees.exclude(status=FeeItem.STATUS_PAID).count(),
    }
    fee_totals['outstanding_display'] = f'£{fee_totals["outstanding_pence"] / 100:.2f}'
    fee_totals['overdue_display'] = f'£{fee_totals["overdue_pence"] / 100:.2f}'

    sessions = AttendanceSession.objects.filter(school=school, session_date=session_date)
    marks = AttendanceMark.objects.filter(session__in=sessions)
    present = marks.filter(status=AttendanceMark.STATUS_PRESENT).count()
    late = marks.filter(status=AttendanceMark.STATUS_LATE).count()
    absent = marks.filter(status=AttendanceMark.STATUS_ABSENT).count()
    mark_total = present + late + absent
    attendance_rate = int((present + late) / mark_total * 100) if mark_total else None

    from teachers.models import TeacherProfile
    teacher_count = TeacherProfile.objects.filter(school=school).count()
    class_count = school.classes.count()

    return {
        'student_count': student_count,
        'enrolled_count': enrolled,
        'teacher_count': teacher_count,
        'class_count': class_count,
        'fee_totals': fee_totals,
        'attendance_rate': attendance_rate,
        'attendance_present': present,
        'attendance_absent': absent,
        'attendance_late': late,
        'session_date': session_date,
        'subscription_tier': school.get_subscription_tier_display(),
    }

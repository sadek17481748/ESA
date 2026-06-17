"""
Assign student reference numbers and weekly leaderboard activity for demo data.

Run: python manage.py seed_leaderboard_week
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from academics.models import ClassGroup
from attendance.models import AttendanceMark, AttendanceSession
from homework.models import Assignment, Submission
from schools.models import School
from students.models import StudentProfile


class Command(BaseCommand):
    help = 'Seeds admission numbers and weekly homework/attendance for homepage leaderboard'

    def handle(self, *args, **options):
        school = School.objects.filter(status=School.STATUS_ACTIVE).first()
        if not school:
            self.stdout.write(self.style.WARNING('No active school found.'))
            return

        students = list(
            StudentProfile.objects.filter(school=school, is_active=True)
            .order_by('last_name', 'first_name')[:30]
        )
        if not students:
            self.stdout.write(self.style.WARNING('No students to seed.'))
            return

        class_group = ClassGroup.objects.filter(school=school).first()
        assignment = Assignment.objects.filter(school=school).first()
        since = timezone.now() - timedelta(days=5)

        for i, student in enumerate(students, start=1):
            if not student.admission_number:
                ref_class = (student.year_group or 'GEN').replace(' ', '')
                student.admission_number = f'ANO-{ref_class}-{i:03d}'
                student.save(update_fields=['admission_number'])

        session = None
        if class_group:
            session, _ = AttendanceSession.objects.get_or_create(
                school=school,
                class_group=class_group,
                session_date=since.date(),
            )

        for rank, student in enumerate(students[:10]):
            hw_count = max(1, 3 - rank // 4)
            att_count = max(1, 2 - rank // 5)
            if assignment:
                for n in range(hw_count):
                    sub, created = Submission.objects.get_or_create(
                        assignment=assignment,
                        student=student,
                        defaults={
                            'status': Submission.STATUS_APPROVED,
                            'submitted_at': since + timedelta(hours=rank + n),
                            'body': 'Seeded submission',
                        },
                    )
                    if not created and sub.submitted_at < since:
                        sub.submitted_at = since + timedelta(hours=rank + n)
                        sub.status = Submission.STATUS_APPROVED
                        sub.save(update_fields=['submitted_at', 'status'])
            if session:
                for _ in range(att_count):
                    AttendanceMark.objects.get_or_create(
                        session=session,
                        student=student,
                        defaults={'status': 'present'},
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Leaderboard seed complete for {min(len(students), 10)} students at {school.name}.',
        ))

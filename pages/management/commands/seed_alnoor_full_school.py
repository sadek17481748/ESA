"""
Seed Al-Noor Academy with Year 7–11 classes, timetables, 30 students + 30 parents per class,
and permanent personal demo accounts (outlook=parent, gmail=teacher).

Run: python manage.py seed_alnoor_full_school
Called from ensure_platform_seed on every deploy — idempotent, preserves existing passwords.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academics.models import ClassEnrollment, ClassGroup, YearGroup
from parents.models import ParentProfile, StudentParentLink
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

from pages.seed_helpers import (
    PERSONAL_PARENT_EMAIL,
    PERSONAL_PARENT_PASSWORD,
    PERSONAL_TEACHER_EMAIL,
    PERSONAL_TEACHER_PASSWORD,
    upsert_user,
)
from pages.timetable_service import (
    create_timetable,
    ensure_school_subjects,
    list_school_subjects,
    save_timetable,
)

User = get_user_model()

SCHOOL_NAME = 'Al-Noor Academy'
STUDENTS_PER_CLASS = 30
DEFAULT_STUDENT_PASSWORD = 'student1234'
DEFAULT_PARENT_PASSWORD = 'parent1234'
DEFAULT_TEACHER_PASSWORD = 'teacher1234'

TEACHER_SPECS = (
    ('ms_fatima', 'Fatima', 'Ahmed', 'Quran'),
    ('mr_ali', 'Ali', 'Hassan', 'Maths'),
    ('mr_yusuf', 'Yusuf', 'Khan', 'Arabic'),
    ('mr_mohammed', 'Mohammed', 'Hussain', 'Quran'),
)

CLASS_SPECS = (
    ('Year 7', 7, '7A', 'ms_fatima'),
    ('Year 7', 7, '7B', 'mr_ali'),
    ('Year 8', 8, '8A', 'mr_yusuf'),
    ('Year 8', 8, '8B', 'ms_fatima'),
    ('Year 9', 9, '9A', 'mr_ali'),
    ('Year 9', 9, '9B', 'mr_yusuf'),
    ('Year 10', 10, '10A', 'ms_fatima'),
    ('Year 10', 10, '10B', 'mr_ali'),
    ('Year 11', 11, '11A', 'mr_yusuf'),
    ('Year 11', 11, '11B', 'mr_ali'),
)

FIRST_NAMES = (
    'Amina', 'Fatima', 'Maryam', 'Sara', 'Hafsa', 'Zainab', 'Aisha', 'Khadija',
    'Ahmed', 'Omar', 'Yusuf', 'Ibrahim', 'Hamza', 'Zaid', 'Khalid', 'Hassan',
    'Ali', 'Adam', 'Idris', 'Bilal', 'Musa', 'Isa', 'Salman', 'Tariq',
    'Layla', 'Noor', 'Sumaya', 'Rania', 'Yasmin', 'Safiya',
)

LAST_NAMES = (
    'Hassan', 'Khan', 'Ahmed', 'Ali', 'Rahman', 'Malik', 'Hussain', 'Siddiqui',
    'Choudhury', 'Begum', 'Patel', 'Shah', 'Qureshi', 'Mahmood', 'Karim',
)


def school_scoped_username(base, school):
    return f'{base}_s{school.pk}'


def weekly_timetable_slots(class_name):
    """A realistic week — varies slightly by class letter."""
    letter = class_name[-1].upper() if class_name else 'A'
    if letter == 'A':
        return (
            (0, '08:30', '09:15', 'Quran', 'ms_fatima'),
            (0, '09:15', '10:00', 'Maths', 'mr_ali'),
            (0, '10:15', '11:00', 'English', 'ms_fatima'),
            (0, '11:00', '11:45', 'Break', None),
            (0, '12:30', '13:15', 'Arabic', 'mr_yusuf'),
            (0, '13:15', '14:00', 'Science', 'mr_ali'),
            (1, '08:30', '09:15', 'Maths', 'mr_ali'),
            (1, '09:15', '10:00', 'English', 'ms_fatima'),
            (1, '10:15', '11:00', 'Science', 'mr_yusuf'),
            (2, '08:30', '09:15', 'Arabic', 'mr_yusuf'),
            (2, '09:15', '10:00', 'Maths', 'mr_ali'),
            (2, '10:15', '11:00', 'Quran', 'ms_fatima'),
            (3, '08:30', '09:15', 'English', 'ms_fatima'),
            (3, '09:15', '10:00', 'Science', 'mr_ali'),
            (3, '10:15', '11:00', 'Alimiyah', 'mr_yusuf'),
            (4, '08:30', '09:15', 'Maths', 'mr_ali'),
            (4, '09:15', '10:00', 'Quran', 'ms_fatima'),
            (4, '10:15', '11:00', 'Break', None),
        )
    return (
        (0, '08:30', '09:15', 'Maths', 'mr_ali'),
        (0, '09:15', '10:00', 'English', 'ms_fatima'),
        (0, '10:15', '11:00', 'Break', None),
        (0, '11:00', '11:45', 'Quran', 'ms_fatima'),
        (1, '08:30', '09:15', 'Science', 'mr_yusuf'),
        (1, '09:15', '10:00', 'Arabic', 'mr_yusuf'),
        (1, '10:15', '11:00', 'Maths', 'mr_ali'),
        (2, '08:30', '09:15', 'English', 'ms_fatima'),
        (2, '09:15', '10:00', 'Quran', 'ms_fatima'),
        (3, '08:30', '09:15', 'Maths', 'mr_ali'),
        (3, '09:15', '10:00', 'Science', 'mr_ali'),
        (4, '08:30', '09:15', 'Arabic', 'mr_yusuf'),
        (4, '09:15', '10:00', 'Alimiyah', 'mr_yusuf'),
        (4, '10:15', '11:00', 'Break', None),
    )


class Command(BaseCommand):
    help = (
        'Seeds Al-Noor Y7–Y11 classes with timetables, 30 students/parents per class, '
        'and permanent msadekhussain outlook/gmail accounts'
    )

    def handle(self, *args, **options):
        school, _ = School.objects.get_or_create(
            name=SCHOOL_NAME,
            defaults={'contact_email': 'admin@alnoor.example'},
        )
        ensure_school_subjects(school)

        already_seeded = StudentProfile.objects.filter(
            school=school,
            admission_number='Y7A-001',
        ).exists()

        if already_seeded:
            self.stdout.write('Full school data exists — syncing personal accounts only.')
            self._ensure_personal_accounts(school)
            return

        teacher_profiles = self._seed_teachers(school)
        class_by_name = self._seed_classes(school, teacher_profiles)
        self._seed_students_and_parents(school, class_by_name)
        self._seed_timetables(school, class_by_name, teacher_profiles)
        personal_teacher, linked_student = self._ensure_personal_accounts(school)

        if personal_teacher and '7A' in class_by_name:
            cg = class_by_name['7A']
            cg.teacher = personal_teacher
            cg.save(update_fields=['teacher'])

        self.stdout.write(self.style.SUCCESS(
            f'Al-Noor full school: {len(class_by_name)} classes, '
            f'{STUDENTS_PER_CLASS} students each, timetables ready.'
        ))
        self._print_login_summary(linked_student)

    def _seed_teachers(self, school):
        profiles = {}
        for base, first, last, subject in TEACHER_SPECS:
            if base == 'mr_mohammed':
                username = 'mr_mohammed'
                email = 'mohammed@alnoor.example'
            else:
                username = school_scoped_username(base, school)
                email = f'{username}@esa.demo'

            user, created = upsert_user(
                username,
                email=email,
                role='teacher',
                password=DEFAULT_TEACHER_PASSWORD,
                school=school,
                first_name=first,
                last_name=last,
            )
            profile, _ = TeacherProfile.objects.get_or_create(
                user=user,
                defaults={'school': school, 'subject': subject},
            )
            profile.school = school
            profile.subject = subject
            profile.save()
            profiles[base] = profile
            self.stdout.write(f'  teacher {username} / {DEFAULT_TEACHER_PASSWORD}' + (' (new)' if created else ''))
        return profiles

    def _seed_classes(self, school, teacher_profiles):
        class_by_name = {}
        for year_name, sort_order, class_name, teacher_key in CLASS_SPECS:
            yg, _ = YearGroup.objects.get_or_create(
                school=school,
                name=year_name,
                defaults={'sort_order': sort_order},
            )
            teacher = teacher_profiles.get(teacher_key)
            cg, created = ClassGroup.objects.get_or_create(
                school=school,
                name=class_name,
                defaults={'year_group': yg, 'teacher': teacher},
            )
            cg.year_group = yg
            if teacher:
                cg.teacher = teacher
            cg.save()
            class_by_name[class_name] = cg
            self.stdout.write(f'  class {class_name} ({year_name})' + (' (new)' if created else ''))
        return class_by_name

    def _seed_students_and_parents(self, school, class_by_name):
        for class_name, class_group in class_by_name.items():
            code = class_name.upper().replace(' ', '')
            for i in range(1, STUDENTS_PER_CLASS + 1):
                first = FIRST_NAMES[(i - 1) % len(FIRST_NAMES)]
                last = LAST_NAMES[((i - 1) * 3) % len(LAST_NAMES)]
                admission = f'{code}-{i:03d}'

                parent_username = f'parent_{code.lower()}_{i:02d}'
                parent_email = f'{parent_username}@alnoor.example'
                parent_user, p_created = upsert_user(
                    parent_username,
                    email=parent_email,
                    role='parent',
                    password=DEFAULT_PARENT_PASSWORD,
                    school=school,
                    first_name=first,
                    last_name=last,
                )
                parent_profile, _ = ParentProfile.objects.get_or_create(
                    user=parent_user,
                    defaults={'school': school},
                )

                student_username = f'student_{code.lower()}_{i:02d}'
                student_email = f'{student_username}@alnoor.example'
                student_user, s_created = upsert_user(
                    student_username,
                    email=student_email,
                    role='student',
                    password=DEFAULT_STUDENT_PASSWORD,
                    school=school,
                    first_name=first,
                    last_name=last,
                )
                student_profile, _ = StudentProfile.objects.get_or_create(
                    user=student_user,
                    defaults={
                        'school': school,
                        'first_name': first,
                        'last_name': last,
                        'year_group': class_group.year_group.name if class_group.year_group else class_name,
                        'admission_number': admission,
                    },
                )
                student_profile.school = school
                student_profile.first_name = first
                student_profile.last_name = last
                student_profile.year_group = (
                    class_group.year_group.name if class_group.year_group else class_name
                )
                student_profile.admission_number = admission
                student_profile.is_active = True
                student_profile.save()

                StudentParentLink.objects.get_or_create(
                    parent=parent_profile,
                    student=student_profile,
                    defaults={'relationship': 'guardian'},
                )
                ClassEnrollment.objects.get_or_create(
                    class_group=class_group,
                    student=student_profile,
                )

            self.stdout.write(f'  {class_name}: {STUDENTS_PER_CLASS} students + parents')

    def _seed_timetables(self, school, class_by_name, teacher_profiles):
        from timetable.models import Timetable

        subjects = {s.name: s for s in list_school_subjects(school)}

        for class_name, class_group in class_by_name.items():
            tt_name = f'{class_name} — Spring term'
            if Timetable.objects.filter(school=school, name=tt_name, is_active=True).exists():
                continue

            timetable = create_timetable(
                school,
                name=tt_name,
                class_group=class_group,
                notes='Ready timetable for demo and assessment',
            )
            payload = []
            for weekday, start, end, subj_name, teacher_key in weekly_timetable_slots(class_name):
                subj = subjects.get(subj_name)
                if not subj:
                    continue
                tp = teacher_profiles.get(teacher_key) if teacher_key else None
                payload.append({
                    'weekday': weekday,
                    'start_time': start,
                    'end_time': end,
                    'subject_id': subj.pk,
                    'teacher_id': tp.pk if tp else None,
                })
            if payload:
                save_timetable(timetable, class_group, payload)
            self.stdout.write(f'  timetable {tt_name} ({len(payload)} slots)')

    def _ensure_personal_accounts(self, school):
        """Permanent outlook=parent, gmail=teacher, linked to first 7A student."""
        linked_student = StudentProfile.objects.filter(
            school=school,
            admission_number='Y7A-001',
        ).select_related('user').first()

        if not linked_student:
            linked_student = StudentProfile.objects.filter(school=school).first()

        teacher_user, t_created = upsert_user(
            PERSONAL_TEACHER_EMAIL,
            email=PERSONAL_TEACHER_EMAIL,
            role='teacher',
            password=PERSONAL_TEACHER_PASSWORD,
            school=school,
            first_name='Mohammed',
            last_name='Hussain',
            force_reset_password=t_created,
        )
        teacher_profile, _ = TeacherProfile.objects.get_or_create(
            user=teacher_user,
            defaults={'school': school, 'subject': 'Maths'},
        )
        teacher_profile.school = school
        teacher_profile.subject = 'Maths'
        teacher_profile.save()

        parent_user, p_created = upsert_user(
            PERSONAL_PARENT_EMAIL,
            email=PERSONAL_PARENT_EMAIL,
            role='parent',
            password=PERSONAL_PARENT_PASSWORD,
            school=school,
            first_name='Mohammed',
            last_name='Hussain',
            force_reset_password=p_created,
        )
        StudentProfile.objects.filter(user=parent_user).delete()

        parent_profile, _ = ParentProfile.objects.get_or_create(
            user=parent_user,
            defaults={'school': school},
        )

        if linked_student:
            StudentParentLink.objects.get_or_create(
                parent=parent_profile,
                student=linked_student,
                defaults={'relationship': 'father'},
            )
            self._add_teacher_to_class_timetable(school, teacher_profile, '7A')

        tag = []
        if t_created:
            tag.append('teacher (new)')
        if p_created:
            tag.append('parent (new)')
        self.stdout.write(
            '  personal accounts' + (f' — {", ".join(tag)}' if tag else ' — synced')
        )
        return teacher_profile, linked_student

    def _add_teacher_to_class_timetable(self, school, teacher_profile, class_name):
        from timetable.models import Timetable, TimetableSlot

        timetable = (
            Timetable.objects.filter(
                school=school,
                class_group__name=class_name,
                is_active=True,
            )
            .order_by('-updated_at')
            .first()
        )
        if not timetable:
            return
        TimetableSlot.objects.filter(
            timetable=timetable,
            subject__name='Maths',
        ).update(teacher=teacher_profile)

    def _print_login_summary(self, linked_student):
        child = ''
        if linked_student:
            child = f' → child {linked_student.full_name} ({linked_student.admission_number})'
        self.stdout.write(self.style.SUCCESS(
            '\nPermanent Al-Noor logins:\n'
            f'  School admin: schooladmin / admin1234\n'
            f'  Parent: {PERSONAL_PARENT_EMAIL} / {PERSONAL_PARENT_PASSWORD}{child}\n'
            f'  Teacher: {PERSONAL_TEACHER_EMAIL} / {PERSONAL_TEACHER_PASSWORD}\n'
            f'  Bulk example: student_7a_01 / {DEFAULT_STUDENT_PASSWORD} · '
            f'parent_7a_01 / {DEFAULT_PARENT_PASSWORD}'
        ))

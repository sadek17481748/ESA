"""
Seed sample year groups, classes, teachers, and timetables for a school.
Run automatically for the registered school-admin school on Heroku boot.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academics.models import ClassGroup, YearGroup
from schools.models import School
from teachers.models import TeacherProfile

from pages.timetable_service import (
    create_timetable,
    ensure_school_subjects,
    list_school_subjects,
    save_timetable,
)

User = get_user_model()

# School admin account that should receive demo timetable data on deploy
PRIMARY_SCHOOL_ADMIN_EMAIL = 'msadekhussain2001@gmail.com'

TEACHER_SPECS = (
    ('ms_fatima', 'Fatima', 'Ahmed', 'Quran'),
    ('mr_ali', 'Ali', 'Hassan', 'Maths'),
    ('mr_yusuf', 'Yusuf', 'Khan', 'Arabic'),
)

CLASS_SPECS = (
    ('Year 7', 7, '7A', 'ms_fatima'),
    ('Year 7', 7, '7B', 'mr_ali'),
    ('Year 8', 8, '8A', 'mr_yusuf'),
    ('Year 11', 11, '11B', 'mr_ali'),
)

TIMETABLE_SPECS = (
    ('7A — Spring term', '7A', (
        (0, '08:30', '09:15', 'Quran', 'ms_fatima'),
        (0, '09:15', '10:00', 'Maths', 'mr_ali'),
        (1, '08:30', '09:15', 'Arabic', 'mr_yusuf'),
        (2, '08:30', '09:15', 'English', 'ms_fatima'),
    )),
    ('7B — Spring term', '7B', (
        (0, '08:30', '09:15', 'Maths', 'mr_ali'),
        (1, '09:15', '10:00', 'Science', 'mr_yusuf'),
    )),
    ('8A — Hifz track', '8A', (
        (0, '08:30', '09:15', 'Quran', 'ms_fatima'),
        (3, '08:30', '09:15', 'Islamic Studies', 'mr_yusuf'),
    )),
)


def school_scoped_username(base, school):
    """Unique teacher username per school (avoids clashing across tenants)."""
    return f'{base}_s{school.pk}'


def seed_timetable_samples_for_school(school, stdout=None):
    """Populate one school with demo teachers, classes, and timetables."""
    write = stdout.write if stdout else print

    if ClassGroup.objects.filter(school=school, name__in=['7A', '7B', '8A', '11B']).count() >= 4:
        write(f'Skip {school.name} — sample classes already exist')
        return

    ensure_school_subjects(school)
    subjects = {s.name: s for s in list_school_subjects(school)}
    teacher_profiles = {}

    for base, first, last, subject in TEACHER_SPECS:
        username = school_scoped_username(base, school)
        email = f'{username}@esa.demo'
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={'email': email},
        )
        user.email = email
        user.first_name = first
        user.last_name = last
        user.role = 'teacher'
        user.school = school
        user.email_verified = True
        user.set_password('teacher1234')
        user.save()
        profile, _ = TeacherProfile.objects.get_or_create(
            user=user,
            defaults={'school': school, 'subject': subject},
        )
        profile.school = school
        profile.subject = subject
        profile.save()
        teacher_profiles[base] = profile
        write(f'  teacher {username} / teacher1234')

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
        if not created:
            cg.year_group = yg
            cg.teacher = teacher
            cg.save()
        class_by_name[class_name] = cg
        write(f'  class {class_name} ({year_name})')

    from timetable.models import Timetable
    for tt_name, class_name, slots in TIMETABLE_SPECS:
        class_group = class_by_name.get(class_name)
        if not class_group:
            continue
        if Timetable.objects.filter(school=school, name=tt_name, is_active=True).exists():
            continue
        timetable = create_timetable(
            school,
            name=tt_name,
            class_group=class_group,
            notes='Sample timetable',
        )
        payload = []
        for weekday, start, end, subj_name, teacher_key in slots:
            subj = subjects.get(subj_name)
            if not subj:
                continue
            tp = teacher_profiles.get(teacher_key)
            payload.append({
                'weekday': weekday,
                'start_time': start,
                'end_time': end,
                'subject_id': subj.pk,
                'teacher_id': tp.pk if tp else None,
            })
        if payload:
            save_timetable(timetable, class_group, payload)
        write(f'  timetable {tt_name} ({len(payload)} slots)')

    write(f'Seeded timetable samples for {school.name}')


class Command(BaseCommand):
    help = 'Adds sample year groups, classes, teachers, and timetables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school',
            default='',
            help='School name (default: primary school-admin school)',
        )

    def handle(self, *args, **options):
        if options['school']:
            schools = School.objects.filter(name=options['school'])
            if not schools.exists():
                self.stderr.write(f'School not found: {options["school"]}')
                return
        else:
            admin = User.objects.filter(
                email__iexact=PRIMARY_SCHOOL_ADMIN_EMAIL,
                role='school_admin',
            ).select_related('school').first()
            if not admin or not admin.school_id:
                self.stdout.write(
                    f'No school linked to {PRIMARY_SCHOOL_ADMIN_EMAIL} — nothing to seed',
                )
                return
            schools = [admin.school]

        for school in schools:
            seed_timetable_samples_for_school(school, stdout=self.stdout)
            self.stdout.write(self.style.SUCCESS(f'Done — {school.name}'))

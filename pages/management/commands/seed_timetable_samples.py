"""
Seed sample year groups, classes, teachers, and timetables for demo schools.
Run: python manage.py seed_timetable_samples
     python manage.py seed_timetable_samples --school "Al-Noor Academy"
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

TEACHERS = (
    ('ms_fatima', 'Fatima', 'Ahmed', 'fatima@esa.demo', 'Quran'),
    ('mr_ali', 'Ali', 'Hassan', 'ali@esa.demo', 'Maths'),
    ('mr_yusuf', 'Yusuf', 'Khan', 'yusuf@esa.demo', 'Arabic'),
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


class Command(BaseCommand):
    help = 'Adds sample year groups, classes, teachers, and timetables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school',
            default='',
            help='School name (default: all schools with fewer than 2 classes)',
        )

    def handle(self, *args, **options):
        if options['school']:
            schools = School.objects.filter(name=options['school'])
            if not schools.exists():
                self.stderr.write(f'School not found: {options["school"]}')
                return
        else:
            schools = School.objects.all()

        for school in schools:
            if not options['school'] and ClassGroup.objects.filter(school=school).count() >= 4:
                self.stdout.write(f'Skip {school.name} — already has classes')
                continue
            self._seed_school(school)

    def _seed_school(self, school):
        ensure_school_subjects(school)
        subjects = {s.name: s for s in list_school_subjects(school)}
        teacher_profiles = {}

        for username, first, last, email, subject in TEACHERS:
            user, created = User.objects.get_or_create(
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
            teacher_profiles[username] = profile
            self.stdout.write(f'  teacher {username}')

        class_by_name = {}
        for year_name, sort_order, class_name, teacher_key in CLASS_SPECS:
            yg, _ = YearGroup.objects.get_or_create(
                school=school,
                name=year_name,
                defaults={'sort_order': sort_order},
            )
            teacher = teacher_profiles.get(teacher_key)
            cg, _ = ClassGroup.objects.get_or_create(
                school=school,
                name=class_name,
                defaults={'year_group': yg, 'teacher': teacher},
            )
            cg.year_group = yg
            cg.teacher = teacher
            cg.save()
            class_by_name[class_name] = cg
            self.stdout.write(f'  class {class_name} ({year_name})')

        for tt_name, class_name, slots in TIMETABLE_SPECS:
            class_group = class_by_name.get(class_name)
            if not class_group:
                continue
            from timetable.models import Timetable
            if Timetable.objects.filter(school=school, name=tt_name, is_active=True).exists():
                continue
            timetable = create_timetable(
                school,
                name=tt_name,
                class_group=class_group,
                notes='Sample timetable for demos',
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
            self.stdout.write(f'  timetable {tt_name} ({len(payload)} slots)')

        self.stdout.write(self.style.SUCCESS(f'Seeded timetable samples for {school.name}'))

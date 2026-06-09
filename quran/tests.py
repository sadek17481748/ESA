"""quran/tests.py"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

from .models import QuranAnnotation, QuranSession
from .services import add_annotation, build_ayah_text, mark_session_reviewed

User = get_user_model()


class QuranSessionTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School')
        self.teacher_user = User.objects.create_user(
            username='qt', password='x', role='teacher', school=self.school,
        )
        self.student_user = User.objects.create_user(
            username='qs', password='x', role='student', school=self.school,
        )
        self.teacher = TeacherProfile.objects.create(school=self.school, user=self.teacher_user)
        self.student = StudentProfile.objects.create(
            school=self.school, user=self.student_user,
            first_name='Sara', last_name='Ali', admission_number='Q1',
        )
        self.session = QuranSession.objects.create(
            school=self.school,
            student=self.student,
            teacher=self.teacher,
            surah_number=1,
            surah_name='Al-Fatiha',
            ayah_start=1,
            ayah_end=2,
            ayah_text=build_ayah_text(1, 1, 2),
        )

    def test_build_ayah_text_includes_arabic(self):
        text = build_ayah_text(1, 1, 1)
        self.assertIn('بِسْمِ', text)

    def test_teacher_can_add_annotation(self):
        ann = add_annotation(
            session=self.session,
            teacher_profile=self.teacher,
            ayah_number=1,
            tag=QuranAnnotation.TAG_TAJWEED,
            timestamp_seconds=Decimal('42.5'),
            comment='Ghunnah too short',
        )
        self.assertEqual(ann.tag, QuranAnnotation.TAG_TAJWEED)
        self.assertEqual(self.session.annotations.count(), 1)

    def test_mark_session_reviewed(self):
        mark_session_reviewed(self.session, self.teacher, notes='Good effort')
        self.session.refresh_from_db()
        self.assertEqual(self.session.status, QuranSession.STATUS_REVIEWED)
        self.assertIsNotNone(self.session.reviewed_at)

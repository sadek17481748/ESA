"""quran/tests.py"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

from .models import QuranAnnotation, QuranSession, QuranSessionPage
from .services import (
    add_annotation,
    build_ayah_text,
    mark_session_reviewed,
    save_page_markup,
)

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
            surah_name='Mushaf',
        )

    def test_save_page_markup(self):
        page = save_page_markup(
            session=self.session,
            para_number=1,
            page_number=2,
            note='Good tajweed on this page',
            highlights=[{'x': 0.1, 'y': 0.2, 'w': 0.3, 'h': 0.05, 'color': '#fff59d'}],
        )
        self.assertEqual(page.note, 'Good tajweed on this page')
        self.assertEqual(len(page.highlights), 1)
        self.assertTrue(
            QuranSessionPage.objects.filter(session=self.session, para_number=1, page_number=2).exists()
        )

    def test_teacher_can_create_mushaf_session(self):
        client = Client()
        client.force_login(self.teacher_user)
        response = client.post('/quran/new/', {'student': self.student.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(QuranSession.objects.filter(student=self.student).count(), 2)

    def test_teacher_can_save_page_via_api(self):
        client = Client()
        client.force_login(self.teacher_user)
        response = client.post(
            f'/quran/session/{self.session.pk}/save/',
            data='{"para_number":1,"page_number":1,"note":"Test","highlights":[]}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(QuranSessionPage.objects.filter(session=self.session).exists())

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

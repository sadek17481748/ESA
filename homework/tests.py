"""
homework/tests.py
Sign-off rules and student submit permissions.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from academics.models import ClassGroup
from homework.models import Assignment, Submission
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile

User = get_user_model()


class HomeworkSignOffTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School')
        self.other_teacher_user = User.objects.create_user(
            username='t2', password='x', role='teacher', school=self.school,
        )
        self.teacher_user = User.objects.create_user(
            username='t1', password='x', role='teacher', school=self.school,
        )
        self.student_user = User.objects.create_user(
            username='s1', password='x', role='student', school=self.school,
        )
        self.teacher = TeacherProfile.objects.create(school=self.school, user=self.teacher_user)
        TeacherProfile.objects.create(school=self.school, user=self.other_teacher_user)
        self.student = StudentProfile.objects.create(
            school=self.school, user=self.student_user,
            first_name='A', last_name='B', admission_number='T1',
        )
        self.class_group = ClassGroup.objects.create(school=self.school, name='7A')
        self.subject = Subject.objects.create(
            school=self.school, name='Quran', track='general', lead_teacher=self.teacher,
        )
        self.assignment = Assignment.objects.create(
            school=self.school,
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher,
            title='Surah Yasin',
            due_date=date.today() + timedelta(days=7),
        )
        self.submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            body='Done',
            status=Submission.STATUS_SUBMITTED,
        )
        self.client = APIClient()

    def test_other_teacher_cannot_sign_off(self):
        self.client.force_authenticate(self.other_teacher_user)
        response = self.client.post(
            f'/api/homework/submissions/{self.submission.pk}/sign_off/',
            {'approve': True},
            format='json',
        )
        # Other teachers do not see submissions outside their classes (404 before sign-off runs)
        self.assertIn(response.status_code, (403, 404))

    def test_assigning_teacher_can_approve(self):
        self.client.force_authenticate(self.teacher_user)
        response = self.client.post(
            f'/api/homework/submissions/{self.submission.pk}/sign_off/',
            {'approve': True, 'note': 'Well done'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, Submission.STATUS_APPROVED)

    def test_student_can_submit(self):
        self.submission.status = Submission.STATUS_DRAFT
        self.submission.body = ''
        self.submission.submitted_at = None
        self.submission.save()
        self.client.force_authenticate(self.student_user)
        response = self.client.post(
            f'/api/homework/submissions/{self.submission.pk}/submit/',
            {'body': 'My answer'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, Submission.STATUS_SUBMITTED)

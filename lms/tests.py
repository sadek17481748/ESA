"""lms/tests.py — subjects, tracks, assignments, and student progress."""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from academics.models import ClassGroup
from lms.models import ClassTrackAssignment, CourseMaterial, CourseSubject, CourseTrack, StudentMaterialProgress
from schools.models import School
from students.models import StudentProfile

User = get_user_model()


class LmsPortalTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        self.school = School.objects.get(name='Al-Noor Academy')
        self.admin = User.objects.get(username='schooladmin')
        self.teacher = User.objects.get(username='mr_mohammed')
        self.student_user = User.objects.get(username='student_alnoor_01')
        self.class_group = ClassGroup.objects.filter(school=self.school).first()
        self.student = StudentProfile.objects.get(user=self.student_user)

    def test_school_admin_creates_subject_and_track(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('lms:subject_create'), {
            'name': 'English',
            'description': 'Core literacy',
        })
        self.assertEqual(response.status_code, 302)
        subject = CourseSubject.objects.get(school=self.school, name='English')
        response = self.client.post(reverse('lms:track_create', args=[subject.pk]), {
            'name': 'Foundation',
            'description': '',
            'sort_order': 0,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CourseTrack.objects.filter(subject=subject, name='Foundation').exists())

    def test_teacher_assigns_track_and_student_sees_progress(self):
        subject = CourseSubject.objects.get(school=self.school, name='Maths')
        track, _ = CourseTrack.objects.get_or_create(subject=subject, name='Higher')
        material, _ = CourseMaterial.objects.get_or_create(
            track=track,
            title='Algebra challenge test',
            defaults={
                'material_type': CourseMaterial.TYPE_LINK,
                'external_url': 'https://example.com/worksheet-test',
            },
        )
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('lms:assign'), {
            'class_group': self.class_group.pk,
            'track': track.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ClassTrackAssignment.objects.filter(class_group=self.class_group, track=track).exists())

        self.client.force_login(self.student_user)
        response = self.client.get(reverse('pages:worksheets'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algebra challenge test')

        response = self.client.post(reverse('lms:mark_complete', args=[material.pk]))
        self.assertEqual(response.status_code, 302)
        progress = StudentMaterialProgress.objects.get(student=self.student, material=material)
        self.assertEqual(progress.progress_percent, 100)
        self.assertEqual(progress.status, StudentMaterialProgress.STATUS_COMPLETED)

"""messaging/tests.py — support cases and school messaging."""
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from messaging.models import SchoolConversation, SupportCase, SupportMessage, TeacherReport
from parents.models import StudentParentLink
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()


class MessagingPortalTests(TestCase):
    def setUp(self):
        call_command('ensure_platform_seed')
        call_command('seed_alnoor_demo')
        self.school = School.objects.get(name='Al-Noor Academy')
        self.parent = User.objects.filter(username='parent_alnoor_01').first() or User.objects.get(username='parent_demo')
        self.teacher = User.objects.filter(username='mr_mohammed').first() or User.objects.get(username='teacher_demo')
        self.admin = User.objects.get(username='schooladmin')
        self.super_admin = User.objects.get(username='super')
        self.teacher_profile = TeacherProfile.objects.get(user=self.teacher)
        self.student = StudentProfile.objects.filter(school=self.school).first()

    def test_parent_opens_support_case(self):
        self.client.force_login(self.parent)
        response = self.client.post(reverse('messaging:support_new'), {
            'subject': 'Login issue',
            'message': 'I cannot reset my password.',
        })
        self.assertEqual(response.status_code, 302)
        case = SupportCase.objects.get(opened_by=self.parent)
        self.assertTrue(case.case_number.startswith('ESA-'))
        self.assertEqual(case.messages.count(), 1)

    def test_super_admin_sees_support_queue(self):
        SupportCase.objects.create(
            case_number='ESA-99999',
            opened_by=self.parent,
            subject='Test case',
        )
        self.client.force_login(self.super_admin)
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ESA-99999')
        self.assertContains(response, 'Support queue')

    def test_parent_messages_teacher(self):
        self.client.force_login(self.parent)
        response = self.client.post(reverse('messaging:school_new'), {
            'subject': 'Question about homework',
            'recipient_kind': 'teacher',
            'teacher': self.teacher_profile.pk,
            'message': 'When is the maths worksheet due?',
        })
        self.assertEqual(response.status_code, 302)
        conv = SchoolConversation.objects.get(created_by=self.parent)
        self.assertEqual(conv.recipient_user, self.teacher)
        self.assertEqual(conv.messages.count(), 1)

    def test_teacher_creates_report_for_student(self):
        student = StudentProfile.objects.filter(school=self.school).first()
        self.client.force_login(self.teacher)
        response = self.client.post(reverse('messaging:report_create'), {
            'student': student.pk,
            'subject_line': 'Spring progress',
            'period_covered': 'Spring 2026',
            'strengths': 'Excellent participation',
            'areas_for_improvement': 'Practice times tables',
            'send_to_parent': True,
        })
        self.assertEqual(response.status_code, 302)
        report = TeacherReport.objects.get(student=student, teacher=self.teacher)
        self.assertEqual(report.subject_line, 'Spring progress')
        link = StudentParentLink.objects.filter(student=student).select_related('parent__user').first()
        self.assertEqual(report.parent, link.parent.user)

    def test_school_admin_inbox_shows_parent_with_child_name(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('messaging:inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Participants')
        self.assertContains(response, 'Hassan')

    def test_school_admin_student_search(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse('messaging:student_search'), {'q': 'Amina'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amina Hassan')
        self.assertContains(response, 'Year 7')

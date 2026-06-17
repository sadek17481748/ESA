"""
Assessment checklist tests — maps to README manual testing rows 1–35.
Run: python manage.py test core_app.assessment_checklist_tests
"""
import io
from datetime import date, time, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from academics.models import ClassEnrollment, ClassGroup, YearGroup
from audit.models import AuditLog
from homework.models import Assignment, Submission
from notifications.models import Notification
from parents.models import ParentProfile, StudentParentLink
from payments.models import FeeItem, Payment
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile
from timetable.models import Timetable, TimetableSlot

User = get_user_model()


class AssessmentChecklistApiTests(TestCase):
    """API and auth rows 1–35 from the assessor manual table."""

    def setUp(self):
        self.school_a = School.objects.create(name='Checklist School A')
        self.school_b = School.objects.create(name='Checklist School B')
        self.super_user = User.objects.create_user(
            username='check_super', password='pass', role='super_admin',
        )
        self.admin_a = User.objects.create_user(
            username='check_admin', password='pass', role='school_admin', school=self.school_a,
        )
        self.teacher_a = User.objects.create_user(
            username='check_teacher', password='pass', role='teacher', school=self.school_a,
        )
        self.parent_a = User.objects.create_user(
            username='check_parent', password='pass', role='parent', school=self.school_a,
        )
        self.student_user = User.objects.create_user(
            username='check_student', password='pass', role='student', school=self.school_a,
        )
        self.teacher_profile = TeacherProfile.objects.create(
            school=self.school_a, user=self.teacher_a, subject='Quran',
        )
        self.student = StudentProfile.objects.create(
            school=self.school_a,
            user=self.student_user,
            first_name='Ali',
            last_name='One',
            admission_number='CHK001',
            year_group='7A',
        )
        self.other_student = StudentProfile.objects.create(
            school=self.school_b,
            first_name='Sara',
            last_name='Two',
            admission_number='CHK002',
        )
        self.yg = YearGroup.objects.create(school=self.school_a, name='Year 7', sort_order=7)
        self.class_a = ClassGroup.objects.create(
            school=self.school_a, name='7A', year_group=self.yg, teacher=self.teacher_profile,
        )
        ClassEnrollment.objects.create(class_group=self.class_a, student=self.student)
        self.subject = Subject.objects.create(
            school=self.school_a, name='Quran', track='general', lead_teacher=self.teacher_profile,
        )
        self.api = APIClient()

    def test_row_01_jwt_login_valid(self):
        response = self.api.post('/api/auth/token/', {
            'username': 'check_teacher', 'password': 'pass',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_row_02_jwt_login_invalid(self):
        response = self.api.post('/api/auth/token/', {
            'username': 'check_teacher', 'password': 'wrong',
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_row_03_accounts_me(self):
        self.api.force_authenticate(self.teacher_a)
        response = self.api.get('/api/accounts/me/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'teacher')
        self.assertEqual(response.data['school'], self.school_a.id)
        self.assertEqual(response.data['school_name'], self.school_a.name)

    def test_row_04_school_admin_tenant_scope(self):
        self.api.force_authenticate(self.admin_a)
        response = self.api.get('/api/schools/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([row['id'] for row in response.data], [self.school_a.id])

    def test_row_05_super_admin_sees_all_schools(self):
        self.api.force_authenticate(self.super_user)
        response = self.api.get('/api/schools/')
        self.assertEqual(response.status_code, 200)
        ids = {row['id'] for row in response.data}
        self.assertIn(self.school_a.id, ids)
        self.assertIn(self.school_b.id, ids)

    def test_row_06_teacher_student_tenant_scope(self):
        self.api.force_authenticate(self.teacher_a)
        response = self.api.get('/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Ali')

    def test_row_07_parent_blocked_from_students_api(self):
        self.api.force_authenticate(self.parent_a)
        response = self.api.get('/api/students/')
        self.assertEqual(response.status_code, 403)

    def test_row_08_register_without_school_rejected(self):
        response = self.api.post('/api/accounts/register/', {
            'username': 'nostudent',
            'email': 'n@s.com',
            'password': 'longpass1',
            'role': 'student',
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('school', response.data)

    def test_row_09_rbac_seed_command(self):
        call_command('seed_rbac_users')
        for username, role in (
            ('super', 'super_admin'),
            ('schooladmin', 'school_admin'),
            ('teacher_demo', 'teacher'),
            ('student_demo', 'student'),
            ('parent_demo', 'parent'),
        ):
            user = User.objects.get(username=username)
            self.assertEqual(user.role, role)

    def test_row_10_tenant_middleware(self):
        client = Client()
        User.objects.create_user(
            username='mw_user', password='pass', role='teacher', school=self.school_a,
            email='mw@esa.demo', email_verified=True,
        )
        client.login(username='mw_user', password='pass')
        response = client.get(reverse('pages:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_row_11_audit_log_on_login(self):
        before = AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN).count()
        client = Client()
        User.objects.create_user(
            username='audit_user', password='pass', role='teacher', school=self.school_a,
            email='au@esa.demo', email_verified=True,
        )
        client.post(reverse('login'), {'username': 'audit_user', 'password': 'pass'})
        after = AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN).count()
        self.assertGreater(after, before)
        log = AuditLog.objects.filter(action=AuditLog.ACTION_LOGIN).order_by('-id').first()
        self.assertEqual(log.school_id, self.school_a.id)

    def test_row_19_teacher_list_tenant_scope(self):
        TeacherProfile.objects.create(
            school=self.school_b,
            user=User.objects.create_user(
                username='other_t', password='x', role='teacher', school=self.school_b,
            ),
            subject='Maths',
        )
        self.api.force_authenticate(self.admin_a)
        response = self.api.get('/api/teachers/')
        self.assertEqual(response.status_code, 200)
        school_ids = {row['school'] for row in response.data}
        self.assertEqual(school_ids, {self.school_a.id})

    def test_row_20_class_groups_tenant_scope(self):
        YearGroup.objects.create(school=self.school_b, name='Year 8', sort_order=8)
        ClassGroup.objects.create(school=self.school_b, name='8A')
        self.api.force_authenticate(self.admin_a)
        response = self.api.get('/api/classes/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(row['school'] == self.school_a.id for row in response.data))

    def test_row_21_school_admin_registers_parent(self):
        self.api.force_authenticate(self.admin_a)
        response = self.api.post('/api/parents/register/', {
            'username': 'new_parent_api',
            'email': 'np@test.com',
            'password': 'securepass1',
            'phone': '07700900001',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='new_parent_api')
        self.assertEqual(user.school_id, self.school_a.id)
        self.assertTrue(ParentProfile.objects.filter(user=user).exists())

    def test_row_23_year_groups_crud(self):
        self.api.force_authenticate(self.admin_a)
        response = self.api.get('/api/classes/year-groups/')
        self.assertEqual(response.status_code, 200)
        response = self.api.post('/api/classes/year-groups/', {
            'name': 'Year 9', 'sort_order': 9,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            YearGroup.objects.filter(school=self.school_a, name='Year 9').exists()
        )

    def test_row_24_enrol_student_rejects_cross_school(self):
        self.api.force_authenticate(self.admin_a)
        response = self.api.post('/api/classes/enrollments/', {
            'class_group': self.class_a.pk,
            'student': self.other_student.pk,
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_row_25_bulk_csv_import(self):
        self.api.force_authenticate(self.admin_a)
        csv_body = 'first_name,last_name,year_group,admission_number\nZain,Ali,7A,CSV001\n'
        upload = io.BytesIO(csv_body.encode('utf-8'))
        upload.name = 'students.csv'
        response = self.api.post('/api/students/import_csv/', {'file': upload}, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created'], 1)
        self.assertTrue(
            StudentProfile.objects.filter(school=self.school_a, admission_number='CSV001').exists()
        )

    def test_row_26_hifz_subject_requires_lead_teacher(self):
        self.api.force_authenticate(self.admin_a)
        response = self.api.post('/api/subjects/', {
            'name': 'Hifz Level 1', 'track': 'hifz',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_row_27_timetable_slot_validation(self):
        timetable = Timetable.objects.create(
            school=self.school_a, name='Week 1', class_group=self.class_a,
        )
        self.api.force_authenticate(self.admin_a)
        response = self.api.post('/api/timetable/', {
            'timetable': timetable.pk,
            'class_group': self.class_a.pk,
            'subject': self.subject.pk,
            'teacher': self.teacher_profile.pk,
            'weekday': 0,
            'start_time': '10:00',
            'end_time': '09:00',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_row_28_teacher_timetable_view(self):
        timetable = Timetable.objects.create(
            school=self.school_a, name='Week 1', class_group=self.class_a,
        )
        TimetableSlot.objects.create(
            school=self.school_a,
            timetable=timetable,
            class_group=self.class_a,
            subject=self.subject,
            teacher=self.teacher_profile,
            weekday=0,
            start_time=time(8, 30),
            end_time=time(9, 15),
        )
        self.api.force_authenticate(self.teacher_a)
        response = self.api.get(f'/api/timetable/?class_group={self.class_a.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_row_29_attendance_rejects_non_enrolled_student(self):
        outsider = StudentProfile.objects.create(
            school=self.school_a,
            first_name='Out',
            last_name='Side',
            admission_number='OUT001',
        )
        self.api.force_authenticate(self.teacher_a)
        response = self.api.post('/api/attendance/sessions/', {
            'class_group': self.class_a.pk,
            'session_date': date.today().isoformat(),
            'marks': [{'student': outsider.pk, 'status': 'present'}],
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_row_30_teacher_creates_assignment(self):
        self.api.force_authenticate(self.teacher_a)
        response = self.api.post('/api/homework/assignments/', {
            'class_group': self.class_a.pk,
            'subject': self.subject.pk,
            'title': 'Surah Yasin',
            'due_date': (date.today() + timedelta(days=7)).isoformat(),
            'assignment_type': 'homework',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        assignment = Assignment.objects.get(title='Surah Yasin')
        self.assertTrue(
            Notification.objects.filter(
                user=self.student_user, notification_type='assignment',
            ).exists()
        )

    def test_row_31_32_33_homework_submit_and_sign_off(self):
        assignment = Assignment.objects.create(
            school=self.school_a,
            class_group=self.class_a,
            subject=self.subject,
            teacher=self.teacher_profile,
            title='Worksheet 1',
            due_date=date.today() + timedelta(days=3),
        )
        submission = Submission.objects.create(
            assignment=assignment,
            student=self.student,
            status=Submission.STATUS_DRAFT,
        )
        self.api.force_authenticate(self.student_user)
        response = self.api.post(
            f'/api/homework/submissions/{submission.pk}/submit/',
            {'body': 'Done'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, Submission.STATUS_SUBMITTED)

        other_teacher = User.objects.create_user(
            username='other_sign', password='x', role='teacher', school=self.school_a,
        )
        TeacherProfile.objects.create(school=self.school_a, user=other_teacher, subject='Maths')
        self.api.force_authenticate(other_teacher)
        response = self.api.post(
            f'/api/homework/submissions/{submission.pk}/sign_off/',
            {'approve': True},
            format='json',
        )
        self.assertIn(response.status_code, (403, 404))

        self.api.force_authenticate(self.teacher_a)
        response = self.api.post(
            f'/api/homework/submissions/{submission.pk}/sign_off/',
            {'approve': True, 'note': 'Good'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, Submission.STATUS_APPROVED)

    def test_row_34_35_notifications(self):
        note = Notification.objects.create(
            user=self.student_user,
            school=self.school_a,
            notification_type='info',
            title='Test',
            message='Hello',
        )
        Notification.objects.create(
            user=self.parent_a,
            school=self.school_a,
            notification_type='info',
            title='Other',
            message='Private',
        )
        self.api.force_authenticate(self.student_user)
        response = self.api.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        response = self.api.post(f'/api/notifications/{note.pk}/mark_read/')
        self.assertEqual(response.status_code, 200)
        note.refresh_from_db()
        self.assertTrue(note.is_read)

    def test_row_24b_student_destroy_crud(self):
        """DELETE — full CRUD evidence (criterion 2.4)."""
        temp = StudentProfile.objects.create(
            school=self.school_a,
            first_name='Temp',
            last_name='Delete',
            admission_number='DEL001',
        )
        self.api.force_authenticate(self.admin_a)
        response = self.api.delete(f'/api/students/{temp.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(StudentProfile.objects.filter(pk=temp.pk).exists())

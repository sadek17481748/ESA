"""exams/tests.py"""
from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from academics.models import ClassEnrollment, ClassGroup
from exams.models import Exam, ExamAnswer, ExamQuestion, ExamResult
from exams.services import auto_mark_mcq, finalise_result, publish_exam, save_student_answers
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile

User = get_user_model()


class ExamSignOffTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School')
        self.teacher_user = User.objects.create_user(
            username='et', password='x', role='teacher', school=self.school,
        )
        self.student_user = User.objects.create_user(
            username='es', password='x', role='student', school=self.school,
        )
        self.teacher = TeacherProfile.objects.create(school=self.school, user=self.teacher_user)
        self.student = StudentProfile.objects.create(
            school=self.school, user=self.student_user,
            first_name='Omar', last_name='Khan', admission_number='E1',
        )
        self.class_group = ClassGroup.objects.create(school=self.school, name='8A')
        ClassEnrollment.objects.create(class_group=self.class_group, student=self.student)
        self.subject = Subject.objects.create(
            school=self.school, name='Islamic Studies', track='general', lead_teacher=self.teacher,
        )
        self.exam = Exam.objects.create(
            school=self.school,
            class_group=self.class_group,
            subject=self.subject,
            teacher=self.teacher,
            title='Term 1 Test',
            exam_date=date.today(),
            status=Exam.STATUS_PUBLISHED,
        )
        self.mcq = ExamQuestion.objects.create(
            exam=self.exam,
            question_type=ExamQuestion.TYPE_MCQ,
            prompt='How many pillars of Islam?',
            option_a='3', option_b='4', option_c='5', option_d='6',
            correct_option='c',
            max_marks=2,
        )
        self.written = ExamQuestion.objects.create(
            exam=self.exam,
            question_type=ExamQuestion.TYPE_WRITTEN,
            prompt='Explain salah.',
            max_marks=8,
        )
        publish_exam(self.exam)
        self.result = ExamResult.objects.get(exam=self.exam, student=self.student)

    def test_mcq_auto_mark(self):
        save_student_answers(self.result, {
            str(self.mcq.pk): {'selected_option': 'c'},
            str(self.written.pk): {'written_answer': 'Five daily prayers.'},
        })
        self.result.refresh_from_db()
        self.assertEqual(self.result.auto_score, Decimal('2'))

    def test_finalise_makes_official(self):
        save_student_answers(self.result, {str(self.mcq.pk): {'selected_option': 'c'}})
        auto_mark_mcq(self.result)
        finalise_result(result=self.result, teacher_profile=self.teacher, comment='Well done')
        self.result.refresh_from_db()
        self.assertTrue(self.result.is_official)
        self.assertEqual(self.result.status, ExamResult.STATUS_FINALISED)

    def test_parent_sees_only_finalised(self):
        draft = ExamResult.objects.filter(status=ExamResult.STATUS_FINALISED)
        self.assertEqual(draft.count(), 0)
        finalise_result(result=self.result, teacher_profile=self.teacher)
        self.assertEqual(
            ExamResult.objects.filter(status=ExamResult.STATUS_FINALISED).count(), 1,
        )

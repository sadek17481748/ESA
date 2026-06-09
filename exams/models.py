"""
exams/models.py
Exam papers, MCQ auto-marking, written manual marks, and teacher finalisation.
"""
from django.db import models

from academics.models import ClassGroup
from schools.models import School
from students.models import StudentProfile
from subjects.models import Subject
from teachers.models import TeacherProfile


class Exam(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='exams')
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=200)
    exam_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return self.title

    @property
    def total_marks(self):
        return sum(q.max_marks for q in self.questions.all())


class ExamQuestion(models.Model):
    TYPE_MCQ = 'mcq'
    TYPE_WRITTEN = 'written'
    TYPE_CHOICES = [
        (TYPE_MCQ, 'Multiple choice'),
        (TYPE_WRITTEN, 'Written'),
    ]
    OPTION_CHOICES = [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    prompt = models.TextField()
    option_a = models.CharField(max_length=300, blank=True)
    option_b = models.CharField(max_length=300, blank=True)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES, blank=True)
    max_marks = models.PositiveSmallIntegerField(default=1)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.get_question_type_display()}: {self.prompt[:40]}'


class ExamResult(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_MARKED = 'marked'
    STATUS_FINALISED = 'finalised'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_MARKED, 'Marked'),
        (STATUS_FINALISED, 'Finalised'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_results')
    auto_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    manual_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    final_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    teacher_comment = models.TextField(blank=True)
    signed_off_by = models.ForeignKey(
        TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='exam_signoffs',
    )
    signed_off_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('exam', 'student')]

    def __str__(self):
        return f'{self.student} — {self.exam.title} ({self.status})'

    @property
    def is_official(self):
        return self.status == self.STATUS_FINALISED and self.signed_off_at is not None


class ExamAnswer(models.Model):
    result = models.ForeignKey(ExamResult, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.CharField(max_length=1, blank=True)
    written_answer = models.TextField(blank=True)
    marks_awarded = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_auto_marked = models.BooleanField(default=False)

    class Meta:
        unique_together = [('result', 'question')]

    def __str__(self):
        return f'Answer for Q{self.question_id}'

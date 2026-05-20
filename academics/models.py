"""
academics/models.py
Year groups, classes, and student enrolment for a school.
"""
from django.db import models

from schools.models import School
from teachers.models import TeacherProfile


class YearGroup(models.Model):
    """e.g. Year 7, Year 8 — ordered list per school."""

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='year_groups')
    name = models.CharField(max_length=80)
    sort_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']
        unique_together = [('school', 'name')]

    def __str__(self):
        return f'{self.name} ({self.school.name})'


class ClassGroup(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=120)
    year_group = models.CharField(max_length=40, blank=True)
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        unique_together = [('school', 'name')]

    def __str__(self):
        return f'{self.name} ({self.school.name})'


class ClassEnrollment(models.Model):
    """Student assigned to a class for the current academic year."""

    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        'students.StudentProfile', on_delete=models.CASCADE, related_name='class_enrollments',
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('class_group', 'student')]

    def __str__(self):
        return f'{self.student} in {self.class_group.name}'

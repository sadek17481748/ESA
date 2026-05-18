from django.db import models

from schools.models import School
from teachers.models import TeacherProfile


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

"""Hifz juz sign-off — teacher verifies a student has passed a juz."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from schools.models import School
from students.models import StudentProfile


class HifzJuzSignOff(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='hifz_signoffs')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='hifz_signoffs')
    juz_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)],
    )
    signed_off_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hifz_signoffs_given',
    )
    signed_off_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-signed_off_at']
        unique_together = [('student', 'juz_number')]

    def __str__(self):
        return f'{self.student.full_name} — Juz {self.juz_number}'

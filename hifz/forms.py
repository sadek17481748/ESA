"""Hifz sign-off form — pick student and juz."""
from django import forms

from pages.behaviour_service import students_for_teacher
from students.models import StudentProfile

JUZ_CHOICES = [(n, f'Juz {n}') for n in range(1, 31)]


class HifzSignOffForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.none(),
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Student',
    )
    juz_number = forms.ChoiceField(
        choices=JUZ_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Juz',
    )

    def __init__(self, school, teacher_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = students_for_teacher(school, teacher_user)

"""quran/forms.py"""
from django import forms

from students.models import StudentProfile

from .models import QuranAnnotation, QuranSession
from .services import SURAH_NAMES, build_ayah_text


class QuranSessionForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=StudentProfile.objects.none())

    class Meta:
        model = QuranSession
        fields = ('student', 'surah_number', 'ayah_start', 'ayah_end')

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = StudentProfile.objects.filter(
            school=school, is_active=True,
        ).order_by('last_name', 'first_name')
        self.fields['surah_number'].widget = forms.Select(
            choices=[(k, f'{k} — {v}') for k, v in SURAH_NAMES.items()],
        )

    def save(self, commit=True, *, school=None, teacher=None):
        instance = super().save(commit=False)
        instance.school = school
        instance.teacher = teacher
        instance.surah_name = SURAH_NAMES.get(instance.surah_number, f'Surah {instance.surah_number}')
        instance.ayah_text = build_ayah_text(
            instance.surah_number, instance.ayah_start, instance.ayah_end,
        )
        if commit:
            instance.save()
        return instance


class QuranAnnotationForm(forms.ModelForm):
    class Meta:
        model = QuranAnnotation
        fields = ('ayah_number', 'tag', 'timestamp_seconds', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2}),
            'timestamp_seconds': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


class StudentAudioForm(forms.Form):
    student_audio = forms.FileField()


class TeacherFeedbackAudioForm(forms.Form):
    teacher_feedback_audio = forms.FileField()
    teacher_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

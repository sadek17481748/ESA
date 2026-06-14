"""quran/forms.py"""
from django import forms

from students.models import StudentProfile

from .models import QuranAnnotation, QuranSession


class QuranSessionForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=StudentProfile.objects.none())

    class Meta:
        model = QuranSession
        fields = ('student',)

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = StudentProfile.objects.filter(
            school=school, is_active=True,
        ).order_by('last_name', 'first_name')
        self.fields['student'].label = 'Student'

    def save(self, commit=True, *, school=None, teacher=None):
        instance = super().save(commit=False)
        instance.school = school
        instance.teacher = teacher
        instance.surah_name = 'Mushaf'
        instance.surah_number = 1
        instance.ayah_start = 1
        instance.ayah_end = 1
        instance.ayah_text = ''
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
    teacher_feedback_audio = forms.FileField(required=False)
    teacher_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

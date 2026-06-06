"""lms/forms.py"""
from django import forms

from academics.models import ClassGroup

from .models import CourseMaterial, CourseSubject, CourseTrack, MaterialSubmission


class CourseSubjectForm(forms.ModelForm):
    class Meta:
        model = CourseSubject
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Maths'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
        }


class CourseTrackForm(forms.ModelForm):
    class Meta:
        model = CourseTrack
        fields = ['name', 'description', 'sort_order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Foundation'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'description', 'material_type', 'file', 'external_url', 'sort_order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'material_type': forms.Select(attrs={'class': 'form-input'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'external_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://'}),
            'sort_order': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class AssignTrackForm(forms.Form):
    class_group = forms.ModelChoiceField(
        queryset=ClassGroup.objects.none(),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    track = forms.ModelChoiceField(
        queryset=CourseTrack.objects.none(),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_group'].queryset = ClassGroup.objects.filter(school=school).order_by('name')
        self.fields['track'].queryset = CourseTrack.objects.filter(
            subject__school=school,
        ).select_related('subject').order_by('subject__name', 'sort_order')


class MaterialSubmissionForm(forms.ModelForm):
    class Meta:
        model = MaterialSubmission
        fields = ['file', 'notes']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Optional note for your teacher'}),
        }

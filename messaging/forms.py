"""messaging/forms.py"""
from django import forms
from django.contrib.auth import get_user_model

from parents.models import StudentParentLink
from students.models import StudentProfile
from teachers.models import TeacherProfile

from .models import SchoolConversation, SupportCase, TeacherReport

User = get_user_model()


class SupportCaseForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Brief summary of your issue'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe the problem'}),
    )


class SupportReplyForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
    )


class NewSchoolMessageForm(forms.Form):
    RECIPIENT_CHOICES = [
        ('school', 'School office'),
        ('teacher', 'A teacher'),
    ]

    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 4}))
    recipient_kind = forms.ChoiceField(
        choices=RECIPIENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Send to',
    )
    teacher = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.none(),
        required=False,
        empty_label='Select teacher',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    parent = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        empty_label='Select parent',
        widget=forms.Select(attrs={'class': 'form-input'}),
        label='Parent',
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        school = user.school
        self.fields['teacher'].queryset = TeacherProfile.objects.filter(school=school).select_related('user')
        self.fields['parent'].queryset = User.objects.filter(role='parent', school=school).order_by('last_name')

        if user.role == 'parent':
            self.fields['recipient_kind'].choices = [
                ('school', 'School office'),
                ('teacher', 'A teacher'),
            ]
        elif user.role == 'teacher':
            self.fields['recipient_kind'].choices = [
                ('school', 'School office'),
                ('parent', 'A parent'),
            ]
        elif user.role == 'school_admin':
            self.fields['recipient_kind'].choices = [
                ('teacher', 'A teacher'),
                ('parent', 'A parent'),
            ]

    def clean(self):
        cleaned = super().clean()
        kind = cleaned.get('recipient_kind')
        if kind == 'teacher' and not cleaned.get('teacher'):
            self.add_error('teacher', 'Select a teacher.')
        if kind == 'parent' and not cleaned.get('parent'):
            self.add_error('parent', 'Select a parent.')
        return cleaned


class SchoolReplyForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}))


class TeacherReportForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.none(),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    subject_line = forms.CharField(
        label='Report title',
        initial='Progress report',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    period_covered = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Spring term 2026'}),
    )
    strengths = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'What is going well?'}),
    )
    areas_for_improvement = forms.CharField(
        label='Areas for improvement',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
    )
    action_required = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Any follow-up needed at home?'}),
    )
    additional_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
    )
    send_to_parent = forms.BooleanField(
        required=False,
        initial=True,
        label='Send copy to linked parent',
    )

    def __init__(self, school, teacher_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from academics.models import ClassGroup
        from teachers.models import TeacherProfile
        profile = TeacherProfile.objects.filter(user=teacher_user).first()
        if profile:
            class_ids = ClassGroup.objects.filter(school=school, teacher=profile).values_list('pk', flat=True)
            student_ids = StudentProfile.objects.filter(
                class_enrollments__class_group_id__in=class_ids,
            ).values_list('pk', flat=True)
            self.fields['student'].queryset = StudentProfile.objects.filter(pk__in=student_ids).distinct()
        else:
            self.fields['student'].queryset = StudentProfile.objects.filter(school=school, is_active=True)

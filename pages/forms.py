"""
pages/forms.py
Web login and registration — public roles only (no super admin on sign-up).
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction

from parents.models import ParentProfile
from schools.models import School
from students.models import StudentProfile
from teachers.models import TeacherProfile

User = get_user_model()

PUBLIC_ROLES = (
    ('school_admin', 'School Admin'),
    ('teacher', 'Teacher'),
    ('parent', 'Parent'),
    ('student', 'Student'),
)


class EsaAuthenticationForm(AuthenticationForm):
    """Login fields styled to match the wireframe form stack."""

    error_messages = {
        'invalid_login': 'Incorrect username or password.',
        'inactive': 'This account is inactive.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'class': 'form-input',
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'class': 'form-input',
        })


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-input'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-input'}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'given-name', 'class': 'form-input'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'family-name', 'class': 'form-input'}),
    )
    role = forms.ChoiceField(
        choices=PUBLIC_ROLES,
        initial='parent',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    school_name = forms.CharField(
        label='School name',
        max_length=200,
        help_text=(
            'School admins: enter your school name to register it on the platform. '
            'Teachers, parents, and students: type your school to join it or create it if needed.'
        ),
        widget=forms.TextInput(attrs={'autocomplete': 'organization', 'class': 'form-input'}),
    )
    password1 = forms.CharField(
        label='Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-input'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_school_name(self):
        name = self.cleaned_data['school_name'].strip()
        if not name:
            raise forms.ValidationError('School name is required.')
        return name

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in dict(PUBLIC_ROLES):
            raise forms.ValidationError('Choose a valid account type.')
        return role

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        name = data['school_name']
        school = School.objects.filter(name__iexact=name).first()
        if not school:
            school = School.objects.create(
                name=name,
                contact_email=data['email'],
            )

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            school=school,
        )

        if user.role == 'parent':
            ParentProfile.objects.get_or_create(
                user=user,
                defaults={'school': school},
            )
        elif user.role == 'student':
            StudentProfile.objects.get_or_create(
                user=user,
                defaults={
                    'school': school,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
            )
        elif user.role == 'teacher':
            TeacherProfile.objects.get_or_create(
                user=user,
                defaults={'school': school},
            )

        return user

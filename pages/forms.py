"""
pages/forms.py
Web login, parent/student registration (pick a school), and separate school sign-up.
"""
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction

from accounts.verification import is_reserved_demo_email
from parents.models import ParentProfile
from schools.models import School
from students.link_service import link_parent_to_student
from students.models import StudentProfile
from academics.models import ClassGroup, YearGroup
from teachers.models import TeacherProfile

User = get_user_model()

DEFAULT_SCHOOL_NAME = 'Al-Noor Academy'

REGISTER_ROLES = (
    ('parent', 'Parent'),
    ('student', 'Student'),
)


def active_schools():
    return School.objects.filter(status=School.STATUS_ACTIVE).order_by('name')


class EsaAuthenticationForm(AuthenticationForm):
    """Login fields styled to match the wireframe form stack."""

    error_messages = {
        'invalid_login': 'Incorrect username or password.',
        'inactive': 'This account is inactive.',
    }

    def clean_username(self):
        return self.cleaned_data.get('username', '').strip()

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
    school = forms.ModelChoiceField(
        queryset=School.objects.none(),
        empty_label='Select your school',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    role = forms.ChoiceField(
        choices=REGISTER_ROLES,
        initial='parent',
        label='I am a',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'given-name', 'class': 'form-input'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'family-name', 'class': 'form-input'}),
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-input'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-input'}),
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
    class_group = forms.ModelChoiceField(
        label='Class',
        queryset=ClassGroup.objects.none(),
        required=False,
        empty_label='Select your class',
        widget=forms.Select(attrs={'class': 'form-input', 'id': 'id_class_group'}),
    )
    link_code = forms.CharField(
        label='Student link code (parents only)',
        required=False,
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Optional — from your school',
            'autocomplete': 'off',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].queryset = active_schools()
        school_id = self.data.get('school') if self.data else None
        if school_id:
            self.fields['class_group'].queryset = ClassGroup.objects.filter(
                school_id=school_id,
            ).order_by('name')

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if is_reserved_demo_email(email):
            raise forms.ValidationError(
                'Use a real email address. Demo addresses are reserved for test accounts.',
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in dict(REGISTER_ROLES):
            raise forms.ValidationError('Choose Parent or Student.')
        return role

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        school = cleaned.get('school')
        class_group = cleaned.get('class_group')
        if role == 'student' and not class_group:
            self.add_error('class_group', 'Students must select a class.')
        if role == 'student' and class_group and school and class_group.school_id != school.pk:
            self.add_error('class_group', 'That class does not belong to the selected school.')
        link_code = cleaned.get('link_code')
        if role == 'student' and link_code:
            self.add_error('link_code', 'Link codes are for parent accounts only.')
        if role == 'parent' and link_code:
            from students.link_service import resolve_link_code
            row = resolve_link_code(link_code)
            if not row:
                self.add_error('link_code', 'Invalid or expired link code.')
            elif school and row.school_id != school.pk:
                self.add_error('link_code', 'This code belongs to a different school.')
        return cleaned

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        school = data['school']

        user = User.objects.create_user(
            username=data['username'].strip(),
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            school=school,
        )

        if user.role == 'parent':
            ParentProfile.objects.create(user=user, school=school)
            link_code = data.get('link_code')
            if link_code:
                link_parent_to_student(
                    parent_user=user,
                    code=link_code,
                    relationship='guardian',
                )
        else:
            profile = StudentProfile.objects.create(
                user=user,
                school=school,
                first_name=user.first_name,
                last_name=user.last_name,
            )
            class_group = data.get('class_group')
            if class_group:
                from pages.enrollment_service import enroll_student
                enroll_student(profile, class_group)

        return user


class SchoolRegisterForm(forms.Form):
    school_name = forms.CharField(
        label='School name',
        max_length=200,
        widget=forms.TextInput(attrs={'autocomplete': 'organization', 'class': 'form-input'}),
    )
    contact_email = forms.EmailField(
        label='School contact email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-input'}),
    )
    first_name = forms.CharField(
        label='Your first name',
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'given-name', 'class': 'form-input'}),
    )
    last_name = forms.CharField(
        label='Your last name',
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'family-name', 'class': 'form-input'}),
    )
    username = forms.CharField(
        label='Admin username',
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-input'}),
    )
    email = forms.EmailField(
        label='Your email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-input'}),
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

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if is_reserved_demo_email(email):
            raise forms.ValidationError(
                'Use a real email address. Demo addresses are reserved for test accounts.',
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_school_name(self):
        name = self.cleaned_data['school_name'].strip()
        if not name:
            raise forms.ValidationError('School name is required.')
        if School.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A school with this name is already registered.')
        return name

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    @transaction.atomic
    def save(self):
        data = self.cleaned_data
        school = School.objects.create(
            name=data['school_name'],
            contact_email=data['contact_email'],
        )
        user = User.objects.create_user(
            username=data['username'].strip(),
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='school_admin',
            school=school,
            email_verified=False,
        )
        return school, user


class AddTeacherForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'autocomplete': 'username'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'autocomplete': 'email'}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'autocomplete': 'given-name'}),
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input', 'autocomplete': 'family-name'}),
    )
    subject = forms.CharField(
        label='Main subject',
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Quran'}),
    )
    password1 = forms.CharField(
        label='Password',
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'autocomplete': 'new-password'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return p2

    @transaction.atomic
    def save(self, school):
        from teachers.models import TeacherProfile

        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role='teacher',
            school=school,
        )
        profile = TeacherProfile.objects.create(
            school=school,
            user=user,
            subject=data.get('subject', ''),
        )
        return user, profile


class CreateSubjectForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Tajweed'}),
    )
    track = forms.ChoiceField(
        choices=[
            ('general', 'General'),
            ('hifz', 'Hifz'),
            ('alimiyah', 'Alimiyah'),
        ],
        initial='general',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional short code'}),
    )

    def clean_name(self):
        return self.cleaned_data['name'].strip()


class TimetableForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Year 7 — Spring term'}),
    )
    class_group = forms.ModelChoiceField(
        label='Class (optional)',
        queryset=ClassGroup.objects.none(),
        required=False,
        empty_label='Whole school / no class',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Optional notes'}),
    )

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_group'].queryset = ClassGroup.objects.filter(
            school=school,
        ).order_by('name')

    def clean_name(self):
        return self.cleaned_data['name'].strip()


class AddClassForm(forms.Form):
    """Single field — e.g. 2C creates class 2C under Year 2."""

    name = forms.CharField(
        label='Class',
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. 2C, 7A, 11B',
        }),
    )
    teacher = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.none(),
        required=False,
        empty_label='Assign teacher later',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.school = school
        if school is not None:
            self.fields['teacher'].queryset = TeacherProfile.objects.filter(
                school=school,
            ).select_related('user').order_by('user__last_name')

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError('Enter a class name (e.g. 2C).')
        return name

    @staticmethod
    def year_group_for_class(class_name):
        """2C → Year 2, 11B → Year 11, otherwise use the class name."""
        match = re.match(r'^(\d+)', class_name.strip())
        if match:
            return f'Year {int(match.group(1))}'
        return class_name.strip()

    @transaction.atomic
    def save(self, school):
        data = self.cleaned_data
        class_name = data['name']
        year_name = self.year_group_for_class(class_name)
        year_group, _ = YearGroup.objects.get_or_create(
            school=school,
            name=year_name,
            defaults={'sort_order': 0},
        )
        if match := re.match(r'^(\d+)', class_name):
            year_group.sort_order = int(match.group(1))
            year_group.save(update_fields=['sort_order'])
        return ClassGroup.objects.create(
            school=school,
            name=class_name,
            year_group=year_group,
            teacher=data.get('teacher'),
        )


class PickClassForm(forms.Form):
    class_group = forms.ModelChoiceField(
        label='Your class',
        queryset=ClassGroup.objects.none(),
        empty_label='Select your class',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_group'].queryset = ClassGroup.objects.filter(
            school=school,
        ).order_by('name')


class BehaviourLogForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=StudentProfile.objects.none(),
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    record_type = forms.ChoiceField(
        choices=[
            ('commendation', 'Commendation'),
            ('incident', 'Incident'),
        ],
        widget=forms.Select(attrs={'class': 'form-input'}),
    )
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-input'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3}))

    def __init__(self, school, teacher_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from pages.behaviour_service import students_for_teacher
        self.fields['student'].queryset = students_for_teacher(school, teacher_user)

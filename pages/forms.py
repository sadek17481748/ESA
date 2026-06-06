"""
pages/forms.py
Web login, parent/student registration (pick a school), and separate school sign-up.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction

from parents.models import ParentProfile
from schools.models import School
from students.models import StudentProfile
from academics.models import ClassGroup
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].queryset = active_schools()
        school_id = self.data.get('school') if self.data else None
        if school_id:
            self.fields['class_group'].queryset = ClassGroup.objects.filter(
                school_id=school_id,
            ).order_by('name')

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
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Year 8'}),
    )
    year_group_name = forms.CharField(
        label='Year group',
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Same as class name if blank'}),
    )
    teacher = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.none(),
        required=False,
        empty_label='Assign teacher later',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = TeacherProfile.objects.filter(
            school=school,
        ).select_related('user').order_by('user__last_name')

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError('Class name is required.')
        return name

    @transaction.atomic
    def save(self, school):
        data = self.cleaned_data
        year_name = (data.get('year_group_name') or data['name']).strip()
        year_group, _ = YearGroup.objects.get_or_create(
            school=school,
            name=year_name,
            defaults={'sort_order': 0},
        )
        return ClassGroup.objects.create(
            school=school,
            name=data['name'],
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

"""accounts/forms_portal.py — portal auth forms."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()


class EsaPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input', 'autocomplete': 'email'})


class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        label='Verification code',
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'autocomplete': 'one-time-code',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
        }),
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip()


class ParentLinkCodeForm(forms.Form):
    code = forms.CharField(
        label='Student link code',
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'e.g. A1B2C3D4',
            'autocomplete': 'off',
        }),
    )
    relationship = forms.ChoiceField(
        choices=[
            ('mother', 'Mother'),
            ('father', 'Father'),
            ('guardian', 'Guardian'),
        ],
        initial='guardian',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()

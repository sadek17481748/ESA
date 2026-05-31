"""payments/forms.py — school admin fee management."""
from datetime import date, timedelta

from django import forms

from students.models import StudentProfile


class SchoolFeeForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        initial='Term tuition',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    amount_pounds = forms.DecimalField(
        label='Amount (£)',
        min_value=0.01,
        decimal_places=2,
        initial='250.00',
        widget=forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
    )
    due_date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
    )
    student = forms.ModelChoiceField(
        label='Student (leave blank for all students)',
        queryset=StudentProfile.objects.none(),
        required=False,
        empty_label='All students',
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = StudentProfile.objects.filter(
            school=school, is_active=True,
        ).order_by('last_name', 'first_name')

    def amount_pence(self):
        return int(self.cleaned_data['amount_pounds'] * 100)

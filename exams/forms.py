"""exams/forms.py"""
from django import forms

from academics.models import ClassGroup
from subjects.models import Subject

from .models import Exam, ExamQuestion


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('title', 'class_group', 'subject', 'exam_date')
        widgets = {'exam_date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, school, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_group'].queryset = ClassGroup.objects.filter(school=school)
        self.fields['subject'].queryset = Subject.objects.filter(school=school)


class ExamQuestionForm(forms.ModelForm):
    class Meta:
        model = ExamQuestion
        fields = (
            'question_type', 'prompt', 'option_a', 'option_b', 'option_c', 'option_d',
            'correct_option', 'max_marks', 'sort_order',
        )
        widgets = {'prompt': forms.Textarea(attrs={'rows': 2})}


class StudentExamForm(forms.Form):
    """Built dynamically in the view from exam questions."""

    def __init__(self, exam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for q in exam.questions.all():
            if q.question_type == ExamQuestion.TYPE_MCQ:
                choices = [
                    ('a', q.option_a), ('b', q.option_b),
                    ('c', q.option_c), ('d', q.option_d),
                ]
                self.fields[f'q_{q.pk}'] = forms.ChoiceField(
                    label=q.prompt,
                    choices=[('', '— Select —')] + [(c[0], f'{c[0].upper()}. {c[1]}') for c in choices if c[1]],
                    required=False,
                )
            else:
                self.fields[f'q_{q.pk}'] = forms.CharField(
                    label=q.prompt,
                    widget=forms.Textarea(attrs={'rows': 3}),
                    required=False,
                )

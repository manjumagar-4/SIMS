from django import forms
from core.models import Exam

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'subject', 'exam_type', 'exam_date', 'max_marks', 'pass_marks', 'academic_year', 'is_active']
        widgets = {
            'name':          forms.TextInput(attrs={'class': 'form-control'}),
            'subject':       forms.Select(attrs={'class': 'form-control'}),
            'exam_type':     forms.Select(attrs={'class': 'form-control'}),
            'exam_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_marks':     forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_marks':    forms.NumberInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024-25'}),
            'is_active':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

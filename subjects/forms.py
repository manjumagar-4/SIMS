from django import forms
from core.models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'course', 'faculty', 'semester', 'credit_hours', 'subject_type', 'full_marks', 'pass_marks', 'is_active']
        widgets = {
            'name':         forms.TextInput(attrs={'class': 'form-control'}),
            'code':         forms.TextInput(attrs={'class': 'form-control'}),
            'course':       forms.Select(attrs={'class': 'form-control'}),
            'faculty':      forms.Select(attrs={'class': 'form-control'}),
            'semester':     forms.NumberInput(attrs={'class': 'form-control'}),
            'credit_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject_type': forms.Select(attrs={'class': 'form-control'}),
            'full_marks':   forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_marks':   forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active':    forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

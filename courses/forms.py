from django import forms
from core.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'duration_years', 'total_semesters', 'description', 'is_active']
        widgets = {
            'name':             forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bachelor of Science in CSIT'}),
            'code':             forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BSCSIT'}),
            'duration_years':   forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'total_semesters':  forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active':        forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


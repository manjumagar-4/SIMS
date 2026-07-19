from django import forms
from core.models import Result

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'exam', 'marks_obtained', 'is_absent', 'remarks']
        widgets = {
            'student':        forms.Select(attrs={'class': 'form-control'}),
            'exam':           forms.Select(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_absent':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'remarks':        forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

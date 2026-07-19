from django import forms
from core.models import Faculty

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'employee_id', 'email', 'phone', 'department', 'designation', 'qualification', 'hire_date', 'is_active']
        widgets = {
            'name':          forms.TextInput(attrs={'class': 'form-control'}),
            'employee_id':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. FAC001'}),
            'email':         forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':         forms.TextInput(attrs={'class': 'form-control'}),
            'department':    forms.TextInput(attrs={'class': 'form-control'}),
            'designation':   forms.Select(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

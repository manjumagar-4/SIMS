from django import forms
from core.models import Student, Course


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email', 'phone',
            'gender', 'date_of_birth', 'address', 'course', 'current_semester',
            'enrollment_year', 'status', 'photo', 'guardian_name', 'guardian_phone',
        ]
        widgets = {
            'student_id':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. STU2024001'}),
            'first_name':      forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':       forms.TextInput(attrs={'class': 'form-control'}),
            'email':           forms.EmailInput(attrs={'class': 'form-control'}),
            'phone':           forms.TextInput(attrs={'class': 'form-control'}),
            'gender':          forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'course':          forms.Select(attrs={'class': 'form-control'}),
            'current_semester':forms.NumberInput(attrs={'class': 'form-control'}),
            'enrollment_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'status':          forms.Select(attrs={'class': 'form-control'}),
            'photo':           forms.FileInput(attrs={'class': 'form-control'}),
            'guardian_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone':  forms.TextInput(attrs={'class': 'form-control'}),
        }

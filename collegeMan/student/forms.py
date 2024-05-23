from django import forms
from .models import Student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'status',
            'roll_no',
            'enrollment_no',
            'branch',
            'semester',
            'mobile_no',
            'email',
            'father_name',
            'mother_name',
            'father_mobile_no',
            'dob',
            'address',
            'adhar_no',
            'pan_no',
            'category',
            'religion',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'status': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'enrollment_no': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'semester': forms.Select(attrs={'class': 'form-control', 'readonly': True}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
            'adhar_no': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_no': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'religion': forms.TextInput(attrs={'class': 'form-control'}),
        }

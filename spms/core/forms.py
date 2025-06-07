from django import forms
from .models import LeaveRequest
from django.contrib.auth.forms import UserCreationForm
from .models import User, EmployeeProfile


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'Employee'),
        ('MANAGER', 'Manager'),
        ('HR', 'HR Manager'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    department = forms.CharField(max_length=100)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'department', 'salary', 'password1', 'password2']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Department



class StaffCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Mark as staff member
        if commit:
            user.save()
            # Create UserProfile if it doesn't exist
            UserProfile.objects.get_or_create(
                user=user,
                department=self.cleaned_data.get('department')
            )
        return user
    
class StaffUpdateForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Safely get the department, creating profile if needed
        profile, created = UserProfile.objects.get_or_create(user=self.instance)
        if profile.department:
            self.fields['department'].initial = profile.department

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.department = self.cleaned_data['department']
            profile.save()
        return user
    

from backend.models import Subject

class SubjectCreationForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject name'}),
        }


from backend.models import Teacher
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth',
            'salary', 'photo', 'subject'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
        }

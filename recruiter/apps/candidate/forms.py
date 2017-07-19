from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CandidateProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

# class UploadForm(forms.ModelForm):
#     class Meta:
#         model = UploadFile
#         fields = ['upload']

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

class CvForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['cv']

class EditForm(forms.ModelForm):
    class Meta: 
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone']

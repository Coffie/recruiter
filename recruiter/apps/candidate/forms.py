from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CandidateProfile, UploadFile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'first_name', 'last_name', 'phone']

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ['upload', 'tags']

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

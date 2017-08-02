from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import CandidateProfile

class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
        widgets = {
        'email': forms.TextInput(attrs={'id':'inputfield'}), 
        'first_name': forms.TextInput(attrs={'id':'inputfield'}),
        'last_name': forms.TextInput(attrs={'id':'inputfield'}),
         }

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id':'inputfield'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id':'inputfield'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

class CvForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['cv', 'user', 'comment']
        exclude = ('user',)
        widgets = {
                'comment': forms.TextInput(attrs={'id':'inputfield'}),
                }
    
class EditForm(forms.ModelForm):
    class Meta: 
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone']

class EditCvForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['cv',]

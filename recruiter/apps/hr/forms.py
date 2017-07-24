from django.contrib.auth import get_user_model

from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'inputfield'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id': 'inputfield'}))

    class Meta:
        model = get_user_model()
        fields = ['email','password']

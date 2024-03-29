from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['username','password', 'first_name','last_name', 'email']

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User
        fields = ['username','password']
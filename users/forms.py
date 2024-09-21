from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='username', max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Логин', 'class': 'input100'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'input100'}))




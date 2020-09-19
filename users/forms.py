from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','lastname','firstname')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='email / username')
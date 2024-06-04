from django.contrib.auth.models import User

from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login-form',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-form',
        'placeholder': 'Enter your password'
    }))

    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login-form',
        'placeholder': 'Enter your password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'register-form',
        'placeholder': 'Confirm your password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'register-form',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'register-form',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'register-form',
                'placeholder': 'Enter your first name'
            }),
        }

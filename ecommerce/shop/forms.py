from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    country = forms.CharField(max_length=300)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'city', 'country', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'first_name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'last_name'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'address'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'city'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'country'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'password1'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'required': True, 'id': 'password2'})


"""class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True, 'id': 'email', 'class': 'form-control', 'required': 'required'}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control', 'required': 'required'}))
"""
User = get_user_model()

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'autofocus': True, 'id': 'username', 'class': 'form-control', 'required': 'required'})
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control', 'required': 'required'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is not associated with any account.')
        return username


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'address', 'city', 'country', 'password1', 'password2')
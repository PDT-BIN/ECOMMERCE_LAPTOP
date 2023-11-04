from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Customer


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username', 'class': 'log-input-field'
    }), required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'class': 'log-input-field'
    }), required=True)

    class Meta:
        model = User
        fields = '__all__'


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username', 'class': 'log-input-field'
    }), required=True)

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email', 'class': 'log-input-field'
    }), required=True)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password', 'class': 'log-input-field'
    }), required=True)

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password Confirmation', 'class': 'log-input-field'
    }), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PersonalForm(forms.ModelForm):
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'ml-4 p-2 border-2 rounded-lg'
    }), required=False)

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'ml-4 p-2 border-2 rounded-lg'
    }), required=False)

    gender = forms.BooleanField(widget=forms.RadioSelect(attrs={
        'class': 'flex ml-4 gap-10'
    }, choices=((True, 'Nam'), (False, 'Nữ'))), required=False)

    birthdate = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'ml-4 p-2 border-2 rounded-lg'
    }), required=False)

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

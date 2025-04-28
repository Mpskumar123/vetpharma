from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Full Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}))
    email = forms.EmailField(required=True, label="Email Address", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message here', 'rows': 5}), required=True, label="Message")

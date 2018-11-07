from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
# from django.contrib.auth.models import User
# from django.conf import settings
from profiles.models import User

class RegistrationForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'First Name'}))
  last_name = forms.CharField(max_length=30, required=True , widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Last Name'}))
  email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'Email Address'}))

  error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
  password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'type':'password', 'class':'form-control', 'placeholder':'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
  password2 = forms.CharField(
        label=("Password Confirmation"),
        widget=forms.PasswordInput(attrs={'type':'password', 'class':'form-control', 'placeholder':'Password Confirmation'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
    )


  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    widgets = {
      'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Username'})
    }

class AuthenticationFormWithInactives(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'type':'password', 'class':'form-control', 'placeholder':'Password'}),
    )
    
    def confirm_login_allowed(self, user):
        pass
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



# Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User Update Form (for username and email)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


# Profile Update Form (only for password update is NOT recommended like this)
# Better way: use set_password() in view
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']


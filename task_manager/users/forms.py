# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class Register(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'last_name',
            'first_name',
            'password1',
            'password2',
        )

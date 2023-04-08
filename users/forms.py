from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'auth__input'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'auth__input'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'auth__input'
        })

    class Meta:
        model = User
        fields = ["username", 'password1', 'password2']

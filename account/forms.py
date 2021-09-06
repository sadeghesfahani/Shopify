from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=60, required=False)
    last_name = forms.CharField(max_length=60, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)



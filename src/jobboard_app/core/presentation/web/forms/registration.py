from django import forms
from django.contrib.auth.models import Group


def get_user_types() -> list:
    user_type_choices = [(group.name, group.name) for group in Group.objects.all()]
    return user_type_choices


class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Enter password: ", widget=forms.PasswordInput, max_length=100)
    email = forms.EmailField(label="Enter email: ")
    role = forms.ChoiceField(label="Choose account type", choices=get_user_types())

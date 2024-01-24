from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import Profile, User, Company


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'inv_code', 'password1', 'password2']


class CompanyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Company
        fields = ['username', 'first_name', 'last_name', 'name', 'email', 'password1', 'password2']

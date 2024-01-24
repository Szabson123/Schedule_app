from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import Profile, User

class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]
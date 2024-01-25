from django import forms
from django.contrib.auth.forms import UserCreationForm
from base.models import Profile, User, Company, InvitationCode


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'inv_code', 'password1', 'password2']

    def clean_inv_code(self):
        inv_code = self.cleaned_data.get('inv_code')
        if not InvitationCode.objects.filter(code=inv_code, is_used=False):
            raise forms.ValidationError("Podany kod jest nieprawidłowy lub został już użyty")
        return inv_code


class CompanyForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Company
        fields = ['username', 'first_name', 'last_name', 'name', 'email', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from base.models import Profile, User, Company, InvitationCode


class UserForm(UserCreationForm):
    inv_code = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'inv_code', 'password1', 'password2']

    def clean_inv_code(self):
        inv_code = self.cleaned_data.get('inv_code')
        if not InvitationCode.objects.filter(code=inv_code, is_used=False):
            raise forms.ValidationError("Podany kod jest nieprawidłowy lub został już użyty")
        return inv_code


class CompanyForm(forms.ModelForm):
    custom_inv_code = forms.CharField(required=True, label="Kod do przyszłego logowania")
    email = forms.EmailField(required=True)

    class Meta:
        model = Company
        fields = ['name', 'email', 'custom_inv_code']


class UserCompanyForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    inv_code = forms.CharField(label="Kod zaproszenia")

    def clean(self):
        cleaned_data = super().clean()
        inv_code = cleaned_data.get('inv_code')

        username = self.cleaned_data.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                if not InvitationCode.objects.filter(user=user, code=inv_code):
                    raise forms.ValidationError("Nieprawidłowy kod zaproszenia")
        return cleaned_data


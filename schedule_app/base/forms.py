from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from base.models import Profile, User, Company, InvitationCode, Event, Availability, Timetable, TimetableSettings
from django.utils.functional import cached_property


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


class CreateEventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
        'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['name', 'description', 'start_time', 'end_time']
        

class CreateAvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        widgets = {
            'availability_day': forms.DateInput(attrs={'type': 'date'}),
            'availability_start': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'availability_end': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
        fields = ['availability_day', 'availability_start', 'availability_end']


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),
            'start': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'end': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
        fields = ['user', 'day', 'start', 'end']


class TimetableSettingsForm(forms.ModelForm):
    class Meta:
        model = TimetableSettings
        fields = ['people', 'start_time', 'end_date', 'work_days', 'justice', 'min_length']


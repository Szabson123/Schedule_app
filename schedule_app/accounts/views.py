from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from base.models import User, Profile, Company, InvitationCode
from base.forms import UserForm, CompanyForm, UserCompanyForm, UserLoginForm


class UserLoginView(LoginView):
    form_class = UserLoginForm


def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            inv_code = form.cleaned_data['inv_code']

            invitation = InvitationCode.objects.create(code=inv_code, is_used=True)

            Profile.objects.create(user=user, inv_code=invitation)

            invitation.user = user
            invitation.save()

            login(request, user)
            return redirect('accounts:login')
    else:
        form = UserForm
    return render(request, 'accounts/register_user.html', {'form': form})


def company_register(request):
    if request.method == 'POST':
        user_form = UserCompanyForm(request.POST)
        company_form = CompanyForm(request.POST)
        
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()

            company = company_form.save(commit=False)
            company.owner = user
            company.save()
            
            custom_inv_code = company_form.cleaned_data['custom_inv_code']
            invitation_code = InvitationCode.objects.create(company=company, code=custom_inv_code, is_used=True)
            Profile.objects.create(user=user, inv_code=invitation_code)

            invitation_code.user = user
            invitation_code.save()

            login(request, user)
            return redirect('accounts:login')
    else:
        user_form = UserCompanyForm()
        company_form = CompanyForm()

    return render(request, 'accounts/register_company.html', {
        'user_form': user_form,
        'company_form': company_form
    })



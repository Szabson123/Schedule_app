from django.shortcuts import render, redirect
from django.contrib.auth import login

from base.models import User, Profile, Company, InvitationCode
from base.forms import UserForm, CompanyForm
from django.contrib.auth.forms import UserCreationForm

def user_register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            inv_code = form.cleaned_data['inv_code']
            invitation = InvitationCode.objects.get(code=inv_code)
            invitation.is_used = True
            invitation.save()

            user = form.save()
            login(request, user)
            return redirect('accounts:login')
    else:
        form = UserForm
    return render(request, 'accounts/register_user.html', {'form': form})


def company_register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        company_form = CompanyForm(request.POST)
        
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            
            company = company_form.save(commit=False)
            company.owner = user
            company.save()
            
            custom_inv_code = company_form.cleaned_data['custom_inv_code']
            company.generate_invitation_code(custom_code=custom_inv_code)
            
            login(request, user)
            return redirect('accounts:login')
    else:
        user_form = UserCreationForm()
        company_form = CompanyForm()
    return render(request, 'accounts/register_company.html', {
    'user_form': user_form,
    'company_form': company_form
    })

from django.shortcuts import render, redirect
from django.contrib.auth import login

from base.models import User, Profile, Company, InvitationCode
from base.forms import UserForm, CompanyForm


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
            return redirect('login')
    else:
        form = UserForm
    return render(request, 'accounts/register_user.html', {'form': form})


def company_register(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            custom_inv_code = form.cleaned_data('custom_inv_code')
            company.owner = request.user
            company.save()
            company.generate_invitation_code(custom_code=custom_inv_code)
            
            login(request, request.user)
            return redirect('login')
    else:
        form = CompanyForm
    return render(request, 'accounts/register_company.html', {'form': form})

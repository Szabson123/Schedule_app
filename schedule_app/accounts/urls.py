from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import user_register, company_register, UserLoginView


app_name = 'accounts'

urlpatterns = [
    path('', UserLoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('user_register/', user_register, name='user_register'),
    path('company_register/', company_register, name='company_register'),
]

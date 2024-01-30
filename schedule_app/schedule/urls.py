from django.urls import path
from schedule.views import main_page

app_name = 'accounts'

urlpatterns = [
    path('main_page/', main_page, name='main_page')
]
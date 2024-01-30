from django.urls import path
from schedule.views import main_page, month_calendar

app_name = 'accounts'

urlpatterns = [
    path('main_page/', main_page, name='main_page'),
    path('month_calendar/<int:year>/<str:month>/', month_calendar, name='month_calendar')
]

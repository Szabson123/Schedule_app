from django.urls import path
from schedule.views import main_page, CalendarView, CreateEventView


app_name = 'schedule'

urlpatterns = [
    path('main_page/', main_page, name='main_page'),
    path('month_calendar/', CalendarView.as_view(), name='month_calendar'),
    path('create_event', CreateEventView.as_view(), name='create_event'),
]

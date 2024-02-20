from django.urls import path
from schedule.views import (main_page, CalendarView,
                            CreateEventView, UpdateEventView,
                            WorkersView, DeleteWorkersView,
                            AvaibilityView, CreateAvaibilityView,
                            TimetableView, TimetableSettingsView)


app_name = 'schedule'

urlpatterns = [
    path('main_page/', main_page, name='main_page'),
    path('month_calendar/', CalendarView.as_view(), name='month_calendar'),
    path('create_event/', CreateEventView.as_view(), name='create_event'),
    path('update_event/<int:pk>/', UpdateEventView.as_view(), name='update_event'),

    path('workers_list/', WorkersView.as_view(), name='workers_view'),
    path('worker_delete/<int:pk>/', DeleteWorkersView.as_view(), name='worker_delete'),
    
    path('avaibility/', AvaibilityView.as_view(), name='avaibility'),
    path('create_avaibility/', CreateAvaibilityView.as_view(), name='create_avaibility'),
    
    path('timetable/', TimetableView.as_view(), name='timetable'),
    
    path('generate/', TimetableSettingsView.as_view(), 'generate')
]

from typing import Any
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from django.views.generic import ListView
from datetime import datetime, date
from django.utils.safestring import mark_safe


from base.models import Event
from schedule.utils import UserCalendar


def main_page(request):
    return render(request, 'schedule/main_page.html')


def month_calendar(request, year, month):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    cal = HTMLCalendar().formatmonth(year, month_number)

    return render(request, 'schedule/month_calendar.html', {
        'month': month,
        'cal': cal
    })


class CalendarView(ListView):
    model = Event
    template_name = 'schedule/month_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        d = self.get_date(self.request.GET.get('day', None))
        
        cal = UserCalendar(d.year, d.month)
        
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

    @staticmethod
    def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today().date()
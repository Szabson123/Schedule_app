from typing import Any
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from django.views.generic import ListView
from datetime import datetime, date
from django.utils.safestring import mark_safe
from datetime import timedelta

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


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(ListView):
    model = Event
    template_name = 'schedule/month_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        d = self.get_date(self.request.GET.get('day', None))
        cal = UserCalendar(d.year, d.month)
        
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

    @staticmethod
    def get_date(req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return datetime.today().date()
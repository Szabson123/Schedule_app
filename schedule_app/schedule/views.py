from typing import Any
from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from django.views.generic import ListView, CreateView
from datetime import datetime, date
from django.utils.safestring import mark_safe
from datetime import timedelta

from base.forms import CreateEventForm
from base.models import Event
from schedule.utils import UserCalendar


def main_page(request):
    return render(request, 'schedule/main_page.html')


class CalendarView(ListView):
    model = Event
    template_name = 'schedule/month_calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = UserCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

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


class CreateEventView(CreateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'schedule/create_event.html'
    success_url = 'month_calendar'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
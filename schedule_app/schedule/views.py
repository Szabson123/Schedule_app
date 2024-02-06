from typing import Any
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView, DeleteView)
from django.utils.safestring import mark_safe

from base.forms import CreateEventForm
from base.models import Event, InvitationCode, Profile, Company
from schedule.utils import UserCalendar

from datetime import datetime, date
import calendar
from calendar import HTMLCalendar
from datetime import timedelta


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
    

class UpdateEventView(UpdateView):
    model = Event
    form_class = CreateEventForm
    template_name = 'schedule/update_event.html'
    
    def get_success_url(self):
        return reverse('schedule:month_calendar')


class WorkersView(ListView):
    model = InvitationCode
    template_name = 'schedule/workers_list.html'
    context_object_name = 'codes'

    def get_queryset(self):
        company = get_object_or_404(Company, owner=self.request.user)
        return InvitationCode.objects.filter(company=company).select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_generate_code_button'] = True
        return context

    def post(self, request, *args, **kwargs):
        company = Company.objects.get(owner=request.user)
        new_code = company.generate_invitation_code()
        return redirect(reverse('schedule:workers_view'))


class DeleteWorkersView(DeleteView):
    model = InvitationCode
    template_name = 'schedule/workers_delete.html'
    success_url = reverse_lazy('schedule:workers_list')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

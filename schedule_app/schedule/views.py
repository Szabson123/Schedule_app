from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, CreateView,
                                  UpdateView, DetailView, DeleteView)
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from base.forms import CreateEventForm, CreateAvailabilityForm
from base.models import Event, InvitationCode, Profile, Company, Availability, Timetable
from schedule.utils import UserCalendar, get_week_dates
from base.decorators import check_user_able_to_see_page

from datetime import datetime, date
import calendar
from calendar import HTMLCalendar
from datetime import timedelta

from django.db.models.functions import TruncDay
from collections import defaultdict

@login_required()
def main_page(request):
    return render(request, 'schedule/main_page.html')


class CalendarView(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'schedule/month_calendar.html'
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        
        cal = UserCalendar(self.request.user, d.year, d.month)
        
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


class CreateEventView(CreateView, LoginRequiredMixin):
    model = Event
    form_class = CreateEventForm
    template_name = 'schedule/create_event.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('schedule:month_calendar')
    

class UpdateEventView(UpdateView, LoginRequiredMixin):
    model = Event
    form_class = CreateEventForm
    template_name = 'schedule/update_event.html'
    
    def get_success_url(self):
        return reverse('schedule:month_calendar')


class WorkersView(ListView, LoginRequiredMixin):
    model = InvitationCode
    template_name = 'schedule/workers_list.html'
    context_object_name = 'codes'

    @method_decorator(check_user_able_to_see_page)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
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


class DeleteWorkersView(LoginRequiredMixin, DeleteView):
    model = InvitationCode
    template_name = 'schedule/workers_delete.html'
    success_url = reverse_lazy('schedule:workers_view')

    def get_queryset(self):
        company = get_object_or_404(Company, owner=self.request.user)
        return InvitationCode.objects.filter(company=company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AvaibilityView(LoginRequiredMixin, ListView):
    template_name = 'schedule/availability.html'
    model = Availability
    context_object_name = 'availabilities'
    
    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user, upload=False)

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        if 'upload_id' in request.POST:
            pk = request.POST.get('upload_id')
            availability = get_object_or_404(Availability, pk=pk, user=request.user)
            availability.upload = True
            availability.save()
            return HttpResponseRedirect(request.path_info)  # Odświeża stronę, zachowując ten sam URL
        return super().post(request, *args, **kwargs)
    

class CreateAvaibilityView(LoginRequiredMixin, CreateView):
    template_name = 'schedule/create_avaibility.html'
    model = Availability
    form_class = CreateAvailabilityForm
    
    def get_success_url(self):
        return reverse('schedule:avaibility')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TimetableView(LoginRequiredMixin, ListView):
    template_name = 'schedule/timetable.html'
    model = Availability
    context_object_name = 'availabilities'
    
    @method_decorator(check_user_able_to_see_page)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        return Availability.objects.filter(upload=True)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now()
        week_dates = get_week_dates(today)
        context['week_dates'] = {date: [] for date in week_dates}  # Utwórz słownik z datami tygodnia

        availabilities = Availability.objects.filter(upload=True)
        
        for availability in availabilities:
            if availability.availability_day in context['week_dates']:
                context['week_dates'][availability.availability_day].append(availability)

        context['days_list'] = Availability.objects.values_list('availability_day', flat=True).distinct()
        context['hours_list'] = Availability.objects.values_list('availability_start', flat=True).distinct()
        return context



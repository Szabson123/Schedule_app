from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar

def main_page(request):
    name = 'Szymon'
    return render(request, 'schedule/main_page.html', {
        'name': name
        #'year': year,
        #'month': month
    })

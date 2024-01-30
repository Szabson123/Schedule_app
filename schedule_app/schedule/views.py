from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar


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

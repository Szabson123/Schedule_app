from datetime import datetime, timedelta
from calendar import HTMLCalendar
from base.models import Event, Timetable
from django.urls import reverse
from django.utils.html import format_html


class UserCalendar(HTMLCalendar):
    def __init__(self, user, year=None, month=None):
        self.user = user
        self.year = year
        self.month = month
        super().__init__()

    def formatday(self, day, events):
        events_start_per_day = events.filter(start_time__day=day)
        events_end_per_day = events.filter(end_time__day=day)
        timetables_for_day = Timetable.objects.filter(user=self.user, day__year=self.year, day__month=self.month, day__day=day)
        
        d = ''
        for event in events_start_per_day:
            event_url = reverse('schedule:update_event', args=(event.id,))
            d += f'<li><a style="color:green; text-decoration:none;" href="{event_url}">{event.name}</a></li>'
        for event in events_end_per_day:
            event_url = reverse('schedule:update_event', args=(event.id,))
            d += f'<li><a style="color:red; text-decoration:none;" href="{event_url}">{event.name}</a></li>'
        
        for timetable in timetables_for_day:
            start_time_formatted = timetable.start.strftime("%H:%M")
            end_time_formatted = timetable.end.strftime("%H:%M")
            d += format_html('<li style="color:brown;">{} - {}</li>', start_time_formatted, end_time_formatted)
        
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(user=self.user, start_time__year=self.year, start_time__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


def get_week_dates(date):
    start_of_week = date.date() - timedelta(days=date.weekday())
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    return week_dates

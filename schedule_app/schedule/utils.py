from datetime import datetime
from calendar import HTMLCalendar


class UserCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(UserCalendar, self).__init__()
    
    def formatday(self, day: int, weekday: int) -> str:
        return super().formatday(day, weekday)
        
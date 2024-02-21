from django.db import models
from django.contrib.auth.models import User

import uuid
from datetime import datetime


class InvitationCode(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code}'
    

class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def generate_invitation_code(self, custom_code=None):
        if custom_code:
            code = custom_code
        else:
            code = uuid.uuid4().hex[:6].upper()
        InvitationCode.objects.create(company=self, code=code)
        return code
    
    def __str__(self) -> str:
        return self.name
        

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inv_code = models.ForeignKey(InvitationCode, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class Timetable(models.Model):
    day = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.day)


class Availability(models.Model):
    availability_day = models.DateField()
    availability_start = models.TimeField()
    availability_end = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.BooleanField(default=False, blank=True, null=True)
    
    def __str__(self):
        return str(self.availability_day)
    
    
class TimetableSettings(models.Model):
    people = models.IntegerField(default=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    work_days = models.JSONField(default=list)
    justice = models.BooleanField(default=True)
    min_length = models.IntegerField(default=4)
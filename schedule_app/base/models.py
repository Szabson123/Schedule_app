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


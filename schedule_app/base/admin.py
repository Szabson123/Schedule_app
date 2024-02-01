from django.contrib import admin
from base import models

admin.site.register(models.Profile)
admin.site.register(models.Company)
admin.site.register(models.InvitationCode)
admin.site.register(models.Event)

# Register your models here.

from django.contrib import admin
from base import models

admin.site.register(models.Profile)
admin.site.register(models.Company)
admin.site.register(models.InvitationCode)


# Register your models here.

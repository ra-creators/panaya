from django.contrib import admin
from .models import ConnectEmails, ConnectUs

# Register your models here.
admin.site.register(ConnectEmails)
admin.site.register(ConnectUs)
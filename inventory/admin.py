from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Cabin)
admin.site.register(models.Cabinorder)
admin.site.register(models.Billing)
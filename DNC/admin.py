from django.contrib import admin
from .models import Samples, Inventory

# Register your models here.
admin.site.register(Samples)
admin.site.register(Inventory)
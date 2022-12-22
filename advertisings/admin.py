from django.contrib import admin
from advertisings.models import Advertising

# Register your models here.


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    pass

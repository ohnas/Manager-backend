from django.contrib import admin
from visits.models import Visit

# Register your models here.


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    pass

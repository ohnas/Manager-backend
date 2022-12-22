from django.contrib import admin
from sites.models import Site

# Register your models here.


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass

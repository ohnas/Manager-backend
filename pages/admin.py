from django.contrib import admin
from pages.models import Page

# Register your models here.


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

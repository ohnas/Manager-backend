from django.contrib import admin
from brands.models import Brand, Data

# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    pass

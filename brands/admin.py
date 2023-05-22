from django.contrib import admin
from brands.models import Brand, BrandData, ExpenseByHand

# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(BrandData)
class DataAdmin(admin.ModelAdmin):
    pass


@admin.register(ExpenseByHand)
class ExpenseByHandAdmin(admin.ModelAdmin):
    pass

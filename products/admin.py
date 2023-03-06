from django.contrib import admin
from products.models import Product, Options

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from sales.models import Brand, Site, Product


# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ("name", "description", "user")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):

    list_display = ("name", "url", "brand")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "price", "brand")

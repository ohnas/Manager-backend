from django.contrib import admin
from sales.models import Sale


# Register your models here.


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "count",
        "price",
        "delivery_price",
        "pay_time",
        "site",
    )

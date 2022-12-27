from rest_framework import serializers
from sales.models import Sale
from products.serializers import ProductSerializer


class SaleSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = (
            "product",
            "count",
            "price",
            "delivery_price",
            "pay_time",
        )

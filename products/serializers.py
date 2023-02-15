from rest_framework.serializers import ModelSerializer
from products.models import Product, Options


class OptionsSerializer(ModelSerializer):
    class Meta:
        model = Options
        fields = (
            "pk",
            "name",
            "product",
            "price",
            "logistic_fee",
            "quantity",
            "gift_quantity",
        )


class ProductSerializer(ModelSerializer):

    # Reverse serializer(without related_name, _set: defalut name)
    options_set = OptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "price",
            "delivery_price",
            "cost",
            "logistic_fee",
            "quantity",
            "gift_quantity",
            "options_set",
        )

from rest_framework.serializers import ModelSerializer
from products.models import Product
from brands.serializers import BrandSerializer


class ProductSerializer(ModelSerializer):

    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "brand",
            "name",
            "cost",
        )

from rest_framework.serializers import ModelSerializer
from brands.models import Brand
from products.serializers import ProductSerializer
from sites.serializers import SiteSerializer


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
        )


class BrandDetailSerializer(ModelSerializer):

    # Reverse serializer(without related_name, _set: defalut name)
    product_set = ProductSerializer(many=True, read_only=True)
    site_set = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "product_set",
            "site_set",
        )

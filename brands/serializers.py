from rest_framework.serializers import ModelSerializer
from brands.models import Brand, ExpenseByHand
from users.serializers import UserSerializer
from products.serializers import ProductDetailSerializer
from sites.serializers import SiteDetailSerializer


class TinyBrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
        )


class BrandSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "description",
            "user",
        )


class BrandDetailSerializer(ModelSerializer):
    # Reverse serializer(without related_name, _set: defalut name)
    product_set = ProductDetailSerializer(many=True, read_only=True)
    site_set = SiteDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
            "description",
            "product_set",
            "site_set",
        )


class ExpenseByHandSerializer(ModelSerializer):
    brand = TinyBrandSerializer(read_only=True)

    class Meta:
        model = ExpenseByHand
        fields = (
            "pk",
            "brand",
            "description",
            "expense_by_hand",
            "date",
        )

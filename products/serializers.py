from rest_framework.serializers import ModelSerializer
from products.models import Product, Options
from brands.models import Brand

# brand 관련 serializer 가 product 쪽에 기재된 이유는:
# brand 쪽에 기재해서 import 할려고 하면 "most likely due to a circular import" 에러가 발생
# 구글링해도 해결방법이 나오지 않아 그냥 brand model 을 이쪽으로 임포트해서 기재하였음
class TinyBrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "pk",
            "name",
        )


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

    brand = TinyBrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "brand",
        )


class ProductDetailSerializer(ModelSerializer):

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

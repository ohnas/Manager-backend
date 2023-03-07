from rest_framework.serializers import ModelSerializer
from products.serializers import TinyBrandSerializer
from pages.models import Page


class PageSerializer(ModelSerializer):

    brand = TinyBrandSerializer(read_only=True)

    class Meta:
        model = Page
        fields = (
            "pk",
            "view",
            "page_date",
            "brand",
        )

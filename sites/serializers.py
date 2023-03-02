from rest_framework.serializers import ModelSerializer
from sites.models import Site
from products.serializers import TinyBrandSerializer


class SiteSerializer(ModelSerializer):

    brand = TinyBrandSerializer(read_only=True)

    class Meta:
        model = Site
        fields = (
            "pk",
            "name",
            "url",
            "kind",
            "brand",
        )


class SiteDetailSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = (
            "pk",
            "name",
            "url",
            "kind",
        )

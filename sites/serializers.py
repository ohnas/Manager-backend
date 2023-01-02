from rest_framework.serializers import ModelSerializer
from sites.models import Site


class SiteSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = (
            "name",
            "url",
        )

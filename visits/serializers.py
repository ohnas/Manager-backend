from rest_framework.serializers import ModelSerializer
from products.serializers import TinyBrandSerializer
from visits.models import Visit


class VisitSerializer(ModelSerializer):

    brand = TinyBrandSerializer(read_only=True)

    class Meta:
        model = Visit
        fields = (
            "pk",
            "num",
            "visit_date",
            "brand",
        )

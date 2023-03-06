from rest_framework.serializers import ModelSerializer
from products.serializers import TinyProductSerializer
from events.models import Event


class EventSerializer(ModelSerializer):

    product = TinyProductSerializer(read_only=True)

    class Meta:
        model = Event
        fields = (
            "pk",
            "name",
            "event_date",
            "product",
        )

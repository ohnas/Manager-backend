from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from brands.models import Brand
from products.models import Product
from events.serializers import EventSerializer

# Create your views here.


class Events(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, brand_pk):
        try:
            return Brand.objects.get(pk=brand_pk)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, brand_pk):
        brand = self.get_object(brand_pk)
        from_date = request.query_params["dateFrom"]
        to_date = request.query_params["dateTo"]
        events = brand.event_set.filter(event_date__range=(from_date, to_date))
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class CreateEvent(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, brand_pk):
        try:
            return Brand.objects.get(pk=brand_pk)
        except Brand.DoesNotExist:
            raise NotFound

    def post(self, request, brand_pk):
        brand = self.get_object(brand_pk)
        name = request.data.get("name")
        product = request.data.get("product")
        event_date = request.data.get("event_date")
        if not name or not product or not event_date:
            raise ParseError
        product = Product.objects.get(pk=product)
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                event = serializer.save(
                    brand=brand,
                    product=product,
                )
                serializer = EventSerializer(event)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from brands.models import Brand
from products.models import Product
from events.models import Event
from events.serializers import EventSerializer
from datetime import datetime, timedelta

# Create your views here.


class EventsCount(APIView):

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

        total_count = brand.event_set.filter(
            event_date__range=(from_date, to_date)
        ).count()

        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        events_count = {
            "sum": total_count,
        }
        for date in date_list:
            count = brand.event_set.filter(event_date=date).count()
            events_count[date] = count
        return Response(events_count)


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

        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        events = {}
        products = brand.product_set.all().values("pk", "name")
        for product in products:
            events[product["name"]] = {}
            for date in date_list:
                current_product = Product.objects.get(pk=product["pk"])
                event_list = current_product.event_set.filter(event_date=date).values(
                    "pk", "name"
                )
                events[product["name"]][date] = event_list
        return Response(events)


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


class UpdateEvent(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                event = serializer.save()
                serializer = EventSerializer(event)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_200_OK)

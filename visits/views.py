from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from brands.models import Brand
from visits.models import Visit
from visits.serializers import VisitSerializer
from datetime import datetime, timedelta

# Create your views here.


class Visits(APIView):

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

        sum = brand.visit_set.filter(visit_date__range=(from_date, to_date)).aggregate(
            Sum("num")
        )

        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        visits = {
            "sum": sum["num__sum"],
        }
        for date in date_list:
            try:
                visit = brand.visit_set.get(visit_date=date)
                pk = visit.pk
                visit_num = visit.num
            except Visit.DoesNotExist:
                pk = "None"
                visit_num = 0
            visits[date] = {
                "pk": pk,
                "num": visit_num,
            }
        return Response(visits)


class CreateVisit(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, brand_pk):
        try:
            return Brand.objects.get(pk=brand_pk)
        except Brand.DoesNotExist:
            raise NotFound

    def post(self, request, brand_pk):
        brand = self.get_object(brand_pk)
        num = request.data.get("num")
        visit_date = request.data.get("visit_date")
        if not num or not visit_date:
            raise ParseError
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                visit = serializer.save(
                    brand=brand,
                )
                serializer = VisitSerializer(visit)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdateVisit(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Visit.objects.get(pk=pk)
        except Visit.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit)
        return Response(serializer.data)

    def put(self, request, pk):
        visit = self.get_object(pk)
        serializer = VisitSerializer(visit, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                visit = serializer.save()
                serializer = VisitSerializer(visit)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

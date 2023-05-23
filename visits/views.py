from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
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


class MonthlyVisitData(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, brand_pk):
        try:
            return Brand.objects.get(pk=brand_pk)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, brand_pk):
        brand = self.get_object(brand_pk)
        from_month = request.query_params["monthFrom"]
        to_month = request.query_params["monthTo"]
        selected_month_from = datetime.strptime(from_month, "%Y-%m")
        selected_month_to = datetime.strptime(to_month, "%Y-%m")
        selected_year_from = selected_month_from.year
        selected_month_from = selected_month_from.month
        selected_month_to = selected_month_to.month
        data = {}
        month_list = []
        while selected_month_from <= selected_month_to:
            month_list.append(f"{selected_year_from}-{selected_month_from}")
            selected_month_from += 1
        for item in month_list:
            year_month = item.split("-")
            year = year_month[0]
            month = year_month[1]
            if brand.visit_set.filter(
                visit_date__year=year, visit_date__month=month
            ).exists():
                visit_month_date = brand.visit_set.filter(
                    visit_date__year=year, visit_date__month=month
                ).aggregate(Sum("num"))
                data[item] = visit_month_date["num__sum"]
            else:
                data[item] = 0

        return Response(data)

from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from brands.models import Brand
from pages.models import Page
from pages.serializers import PageSerializer
from datetime import datetime, timedelta

# Create your views here.


class Pages(APIView):
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

        sum = brand.page_set.filter(page_date__range=(from_date, to_date)).aggregate(
            Sum("view")
        )

        selected_date_from = datetime.strptime(from_date, "%Y-%m-%d")
        selected_date_to = datetime.strptime(to_date, "%Y-%m-%d")
        delta = timedelta(days=1)
        date_list = []
        while selected_date_from <= selected_date_to:
            date_list.append(selected_date_from.strftime("%Y-%m-%d"))
            selected_date_from += delta
        pages = {
            "sum": sum["view__sum"],
        }
        for date in date_list:
            try:
                page = brand.page_set.get(page_date=date)
                pk = page.pk
                page_view = page.view
            except Page.DoesNotExist:
                pk = "None"
                page_view = 0
            pages[date] = {
                "pk": pk,
                "view": page_view,
            }
        return Response(pages)


class CreatePage(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, brand_pk):
        try:
            return Brand.objects.get(pk=brand_pk)
        except Brand.DoesNotExist:
            raise NotFound

    def post(self, request, brand_pk):
        brand = self.get_object(brand_pk)
        view = request.data.get("view")
        page_date = request.data.get("page_date")
        if not view or not page_date:
            raise ParseError
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                page = serializer.save(
                    brand=brand,
                )
                serializer = PageSerializer(page)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdatePage(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Page.objects.get(pk=pk)
        except Page.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        page = self.get_object(pk)
        serializer = PageSerializer(page)
        return Response(serializer.data)

    def put(self, request, pk):
        page = self.get_object(pk)
        serializer = PageSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                page = serializer.save()
                serializer = PageSerializer(page)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class MonthlyPageData(APIView):
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
            if brand.page_set.filter(
                page_date__year=year, page_date__month=month
            ).exists():
                page_month_date = brand.page_set.filter(
                    page_date__year=year, page_date__month=month
                ).aggregate(Sum("view"))
                data[item] = page_month_date["view__sum"]
            else:
                data[item] = 0

        return Response(data)

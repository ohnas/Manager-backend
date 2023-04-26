from django.db import transaction
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
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
                page_view = page.view
            except Page.DoesNotExist:
                page_view = 0
            pages[date] = page_view
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
        is_page = Page.objects.filter(page_date=page_date, brand=brand)
        if is_page.exists():
            raise ParseError("page is already.")
        else:
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

    def delete(self, request, pk):
        page = self.get_object(pk)
        page.delete()
        return Response(status=status.HTTP_200_OK)

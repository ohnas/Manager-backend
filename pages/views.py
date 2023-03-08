from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from brands.models import Brand
from pages.models import Page
from pages.serializers import PageSerializer

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
        page = brand.page_set.filter(page_date__range=(from_date, to_date))
        serializer = PageSerializer(page, many=True)
        return Response(serializer.data)


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

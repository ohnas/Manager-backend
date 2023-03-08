from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from brands.models import Brand
from visits.models import Visit
from visits.serializers import VisitSerializer

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
        visit = brand.visit_set.filter(visit_date__range=(from_date, to_date))
        serializer = VisitSerializer(visit, many=True)
        return Response(serializer.data)


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
        is_vist = Visit.objects.filter(visit_date=visit_date, brand=brand)
        if is_vist.exists():
            raise ParseError("visit is already.")
        else:
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

    def delete(self, request, pk):
        visit = self.get_object(pk)
        visit.delete()
        return Response(status=status.HTTP_200_OK)

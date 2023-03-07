from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from brands.models import Brand
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

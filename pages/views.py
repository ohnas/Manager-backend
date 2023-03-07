from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from brands.models import Brand
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

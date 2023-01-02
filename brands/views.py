from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from brands.serializers import BrandSerializer, BrandDetailSerializer
from brands.models import Brand


class Brands(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        brands = Brand.objects.filter(user=request.user.pk)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class BrandDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, brand_name):
        try:
            return Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            raise NotFound

    def get(self, request, brand_name):
        brand = self.get_object(brand_name)
        serializer = BrandDetailSerializer(brand)
        return Response(serializer.data)

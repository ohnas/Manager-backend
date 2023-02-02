from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ParseError
from products.serializers import ProductSerializer
from products.models import Product
from brands.models import Brand
from brands.serializers import BrandSerializer


class CreateProduct(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        cost = request.data.get("cost")
        brand = request.data.get("brand")
        if not name or not cost or not brand:
            raise ParseError
        brand = Brand.objects.get(pk=brand)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                product = serializer.save(brand=brand)
                serializer = ProductSerializer(product)
                return Response(serializer.data)

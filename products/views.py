from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from products.serializers import ProductSerializer
from products.models import Product
from brands.models import Brand


class Products(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            brand_name = request.query_params["brand"]
            brand = Brand.objects.get(name=brand_name)
            products = Product.objects.filter(brand=brand.pk)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Brand.DoesNotExist:
            raise NotFound

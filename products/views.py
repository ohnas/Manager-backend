from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ParseError, NotFound
from brands.serializers import BrandSerializer
from products.serializers import ProductSerializer, OptionsSerializer
from products.models import Product
from brands.models import Brand


class Products(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_products = Product.objects.all()
        serializer = ProductSerializer(all_products, many=True)
        return Response(serializer.data)


class CreateProduct(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        cost = request.data.get("cost")
        price = request.data.get("price")
        delivery_price = request.data.get("delivery_price")
        brand = request.data.get("brand")
        if not name or not cost or not brand or not delivery_price or not price:
            raise ParseError
        brand = Brand.objects.get(pk=brand)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                product = serializer.save(brand=brand)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UpdateProduct(APIView):

    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        brand = request.data.get("brand")
        if brand is None:
            if serializer.is_valid():
                with transaction.atomic():
                    product = serializer.save()
                    serializer = ProductSerializer(product)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            brand = Brand.objects.get(pk=brand)
            if serializer.is_valid():
                with transaction.atomic():
                    product = serializer.save(brand=brand)
                    serializer = ProductSerializer(product)
                    return Response(serializer.data)
            else:
                return Response(serializer.errors)


class CreateOption(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_products = Product.objects.all()
        serializer = ProductSerializer(all_products, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        price = request.data.get("price")
        logistic_fee = request.data.get("logistic_fee")
        quantity = request.data.get("quantity")
        gift_quantity = request.data.get("gift_quantity")
        product = request.data.get("product")
        if (
            not name
            or not price
            or not logistic_fee
            or not quantity
            or not gift_quantity
            or not product
        ):
            raise ParseError
        product = Product.objects.get(pk=product)
        serializer = OptionsSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                option = serializer.save(product=product)
                serializer = OptionsSerializer(option)
                return Response(serializer.data)
        else:
            return Response(serializer.errors)

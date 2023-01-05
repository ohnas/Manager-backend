from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound, ParseError
from brands.serializers import BrandSerializer, BrandDetailSerializer
from brands.models import Brand
from users.serializers import UserSerializer
from users.models import User


class Brands(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_brands = Brand.objects.all()
        serializer = BrandSerializer(all_brands, many=True)
        return Response(serializer.data)


class MyBrand(APIView):

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


class CreateBrand(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get("name")
        user = request.data.get("user")
        if not name or not user:
            raise ParseError
        user = User.objects.get(pk=user)
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                brand = serializer.save(user=user)
                serializer = BrandSerializer(brand)
                return Response(serializer.data)

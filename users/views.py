from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.serializers import UserSerializer
from users.models import User
from brands.serializers import BrandSerializer


class BrandByUser(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = self.get_object(pk)
        if user != request.user:
            raise PermissionDenied
        brands = user.brand_set.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


class CreateUser(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        name = request.data.get("name")
        email = request.data.get("email")
        if not username or not password or not name or not email:
            raise ParseError
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                user.set_password(password)
                user.save()
                return Response({"response": "success"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"response": "success"}, status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"response": "success"}, status=status.HTTP_200_OK)

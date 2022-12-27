from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

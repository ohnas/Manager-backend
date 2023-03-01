from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer


class Users(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)


class UserProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)


class CreateUser(APIView):

    # to-do : user 의 is_active 을 활용해서 첫 회원가입시 is_active의 값을 false로 설정하고 관리자 페이지에서 관리자가 true로 변경해야지만 웹사이트 활동 가능하게 로직구현
    # 그리고 관리자 페이지에서 알수없는 사용자가 가입하였을 경우에는 관리자가 삭제 해서 웹사이트 접속자체를 할 수 없도록 구현하기
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
                return Response(serializer.data)
        else:
            return Response(serializer.errors)


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

from django.urls import path
from users.views import LogIn, LogOut, CreateUser, BrandByUser, UserProfile

urlpatterns = [
    path("<int:pk>", UserProfile.as_view()),
    path("<int:pk>/brands", BrandByUser.as_view()),
    path("create", CreateUser.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
]

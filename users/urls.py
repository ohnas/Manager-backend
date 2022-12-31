from django.urls import path
from users.views import LogIn, LogOut, CreateUser, UserProfile

urlpatterns = [
    path("", UserProfile.as_view()),
    path("create", CreateUser.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
]

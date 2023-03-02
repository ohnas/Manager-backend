from django.urls import path
from users.views import (
    LogIn,
    LogOut,
    CreateUser,
    UserProfile,
    Users,
    UpdateUser,
    InactiveUser,
)

urlpatterns = [
    path("", UserProfile.as_view()),
    path("all", Users.as_view()),
    path("create", CreateUser.as_view()),
    path("update/<int:pk>", UpdateUser.as_view()),
    path("inactive", InactiveUser.as_view()),
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
]

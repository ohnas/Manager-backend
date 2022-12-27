from django.urls import path
from users.views import LogIn, LogOut

urlpatterns = [
    path("log-in", LogIn.as_view()),
    path("log-out", LogOut.as_view()),
]

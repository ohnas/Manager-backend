from django.urls import path
from advertisings.views import Advertisings

urlpatterns = [
    path("", Advertisings.as_view()),
]

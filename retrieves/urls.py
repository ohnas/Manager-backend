from django.urls import path
from retrieves.views import Retrieves


urlpatterns = [
    path("", Retrieves.as_view()),
]

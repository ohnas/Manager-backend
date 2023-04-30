from django.urls import path
from retrieves.views import Retrieves, Unlistings


urlpatterns = [
    path("", Retrieves.as_view()),
    path("<int:pk>/unlisting", Unlistings.as_view()),
]

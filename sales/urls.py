from django.urls import path
from sales.views import Sales


urlpatterns = [
    path("@<str:brandname>/<int:pk>", Sales.as_view()),
]

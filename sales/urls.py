from django.urls import path
from sales.views import Sales


urlpatterns = [
    path("", Sales.as_view()),
]

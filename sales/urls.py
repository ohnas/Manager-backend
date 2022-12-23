from django.urls import path
from sales.views import Sales


urlpatterns = [
    path("npr", Sales.as_view()),
]

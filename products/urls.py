from django.urls import path
from products.views import Products

urlpatterns = [
    path("", Products.as_view()),
]

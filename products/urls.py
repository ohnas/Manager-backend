from django.urls import path
from products.views import CreateProduct, Products

urlpatterns = [
    path("", Products.as_view()),
    path("create", CreateProduct.as_view()),
]

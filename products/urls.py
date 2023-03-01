from django.urls import path
from products.views import CreateProduct, CreateOption, Products, UpdateProduct

urlpatterns = [
    path("", Products.as_view()),
    path("create/product", CreateProduct.as_view()),
    path("update/product/<int:pk>", UpdateProduct.as_view()),
    path("create/option", CreateOption.as_view()),
]

from django.urls import path
from products.views import CreateProduct, CreateOption

urlpatterns = [
    path("create/product", CreateProduct.as_view()),
    path("create/option", CreateOption.as_view()),
]

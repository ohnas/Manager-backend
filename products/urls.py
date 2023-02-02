from django.urls import path
from products.views import CreateProduct

urlpatterns = [
    path("create", CreateProduct.as_view()),
]

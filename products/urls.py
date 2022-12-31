from django.urls import path
from products.views import Products

urlpatterns = [
    path("<int:brand_pk>", Products.as_view()),
]

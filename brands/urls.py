from django.urls import path
from brands.views import Brands, BrandDetail

urlpatterns = [
    path("", Brands.as_view()),
    path("<int:pk>", BrandDetail.as_view()),
]

from django.urls import path
from brands.views import Brands, BrandDetail, CreateBrand

urlpatterns = [
    path("", Brands.as_view()),
    path("create", CreateBrand.as_view()),
    path("@<str:brand_name>", BrandDetail.as_view()),
]
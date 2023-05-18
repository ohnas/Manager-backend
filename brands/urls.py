from django.urls import path
from brands.views import (
    Brands,
    MyBrand,
    BrandDetail,
    CreateBrand,
    UpdateBrand,
    MonthlyBrandData,
)

urlpatterns = [
    path("", Brands.as_view()),
    path("my", MyBrand.as_view()),
    path("<int:pk>", BrandDetail.as_view()),
    path("create", CreateBrand.as_view()),
    path("update/<int:pk>", UpdateBrand.as_view()),
    path("<int:pk>/monthly", MonthlyBrandData.as_view()),
]

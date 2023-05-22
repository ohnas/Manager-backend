from django.urls import path
from brands.views import (
    Brands,
    MyBrand,
    BrandDetail,
    CreateBrand,
    UpdateBrand,
    MonthlyBrandData,
    CreateExpenseByHand,
    UpdateExpenseByHand,
)

urlpatterns = [
    path("", Brands.as_view()),
    path("my", MyBrand.as_view()),
    path("<int:pk>", BrandDetail.as_view()),
    path("create", CreateBrand.as_view()),
    path("update/<int:pk>", UpdateBrand.as_view()),
    path("<int:pk>/monthly", MonthlyBrandData.as_view()),
    path("create/expense", CreateExpenseByHand.as_view()),
    path("update/expense/<int:pk>", UpdateExpenseByHand.as_view()),
]

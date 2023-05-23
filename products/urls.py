from django.urls import path
from products.views import (
    CreateProduct,
    CreateOption,
    Products,
    UpdateProduct,
    Option,
    UpdateOption,
    MonthlyProductData,
)

urlpatterns = [
    path("<int:brand_pk>", Products.as_view()),
    path("create/product", CreateProduct.as_view()),
    path("update/product/<int:pk>", UpdateProduct.as_view()),
    path("options/<int:product_pk>", Option.as_view()),
    path("create/option", CreateOption.as_view()),
    path("update/option/<int:pk>", UpdateOption.as_view()),
    path("<int:brand_pk>/monthly", MonthlyProductData.as_view()),
]

from django.urls import path
from brands.views import BrandDetail

urlpatterns = [path("<int:pk>", BrandDetail.as_view())]

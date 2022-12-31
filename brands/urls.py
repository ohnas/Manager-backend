from django.urls import path
from brands.views import Brands

urlpatterns = [path("", Brands.as_view())]

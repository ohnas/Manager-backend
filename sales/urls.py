from django.urls import path
from sales.views import sale_retrieve


urlpatterns = [
    path("npr", sale_retrieve),
]

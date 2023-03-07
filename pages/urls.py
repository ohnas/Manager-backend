from django.urls import path
from pages.views import Pages

urlpatterns = [
    path("<int:brand_pk>", Pages.as_view()),
]

from django.urls import path
from pages.views import Pages, CreatePage, UpdatePage

urlpatterns = [
    path("<int:brand_pk>", Pages.as_view()),
    path("<int:brand_pk>/create", CreatePage.as_view()),
    path("update/<int:pk>", UpdatePage.as_view()),
]

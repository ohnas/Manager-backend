from django.urls import path
from sites.views import CreateSite, Sites, UpdateSite

urlpatterns = [
    path("<int:brand_pk>", Sites.as_view()),
    path("create", CreateSite.as_view()),
    path("update/<int:pk>", UpdateSite.as_view()),
]

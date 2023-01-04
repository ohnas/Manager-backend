from django.urls import path
from sites.views import CreateSite

urlpatterns = [
    path("create", CreateSite.as_view()),
]

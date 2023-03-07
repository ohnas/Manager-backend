from django.urls import path
from visits.views import Visits

urlpatterns = [
    path("<int:brand_pk>", Visits.as_view()),
]

from django.urls import path
from visits.views import Visits, CreateVisit, UpdateVisit, MonthlyVisitData

urlpatterns = [
    path("<int:brand_pk>", Visits.as_view()),
    path("<int:brand_pk>/create", CreateVisit.as_view()),
    path("update/<int:pk>", UpdateVisit.as_view()),
    path("<int:brand_pk>/monthly", MonthlyVisitData.as_view()),
]

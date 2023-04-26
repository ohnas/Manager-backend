from django.urls import path
from events.views import EventsCount, CreateEvent, UpdateEvent

urlpatterns = [
    path("<int:brand_pk>/count", EventsCount.as_view()),
    path("<int:brand_pk>/create", CreateEvent.as_view()),
    path("update/<int:pk>", UpdateEvent.as_view()),
]

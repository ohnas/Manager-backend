from django.urls import path
from events.views import Events, CreateEvent, UpdateEvent, EventsCount

urlpatterns = [
    path("<int:brand_pk>", Events.as_view()),
    path("<int:brand_pk>/count", EventsCount.as_view()),
    path("<int:brand_pk>/create", CreateEvent.as_view()),
    path("update/<int:pk>", UpdateEvent.as_view()),
]

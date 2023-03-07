from django.urls import path
from events.views import Events, CreateEvent

urlpatterns = [
    path("<int:brand_pk>", Events.as_view()),
    path("<int:brand_pk>/create", CreateEvent.as_view()),
]

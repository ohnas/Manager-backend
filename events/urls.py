from django.urls import path
from events.views import Events

urlpatterns = [
    path("<int:brand_pk>", Events.as_view()),
]

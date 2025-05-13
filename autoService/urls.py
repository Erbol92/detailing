from django.urls import path
from .views import service, service_detail, calendar_events

urlpatterns = [
    path('service', service, name='service'),
    path('service/<int:pk>', service_detail, name='service_detail'),
    path('calendar_events', calendar_events, name='calendar_events'),
]
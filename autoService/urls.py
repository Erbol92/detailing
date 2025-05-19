from django.urls import path

from .views import service, service_detail, calendar_events, get_schedule_work, get_schedule_record

urlpatterns = [
    path('service', service, name='service'),
    path('service/<int:pk>', service_detail, name='service_detail'),
    path('calendar_events', calendar_events, name='calendar_events'),
    path('get_schedule_work/', get_schedule_work, name='get_schedule_work'),
    path('get_schedule_record/', get_schedule_record, name='get_schedule_record'),
]

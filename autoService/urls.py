from django.urls import path
from .views import service, service_detail

urlpatterns = [
    path('service', service, name='service'),
    path('service/<int:pk>', service_detail, name='service_detail'),
]
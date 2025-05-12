from django.urls import path

from .views import main, user_logout, profile, get_models, request_auth_form_processor

urlpatterns = [
    path('', main, name='main'),
    path('user_logout', user_logout, name='user_logout'),
    path('profile', profile, name='profile'),
    path('get_models', get_models, name='get_models'),
    path('request_auth_form_processor', request_auth_form_processor, name='request_auth_form_processor')
]

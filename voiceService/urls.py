from django.urls import path

from .views import voice_register, VoiceDetailView, create_update_voice, closing_voice

urlpatterns = [
    path('voice_register', voice_register, name='voice_register'),
    path('voices/<int:pk>/', VoiceDetailView.as_view(), name='voice_detail'),
    path('create_update_voice/<int:voice_id>/', create_update_voice, name='create_update_voice'),
    path('closing_voice/<int:voice_id>/', closing_voice, name='closing_voice'),

]

from django.urls import path


from .views import report_main, user_voice_report, generate_inquiries_report, profit_report, master_service_report

urlpatterns = [
    path('', report_main, name='report_main'),
    path('user_voice_report', user_voice_report, name='user_voice_report'),
    path('generate_inquiries_report', generate_inquiries_report, name='generate_inquiries_report'),
    path('profit_report', profit_report, name='profit_report'),
    path('master_service_report', master_service_report, name='master_service_report'),

]

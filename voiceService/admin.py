from django.contrib import admin

from .models import Voice, Topic, VoiceAssignment


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', ]


# Register your models here.
@admin.register(Voice)
class VoiceAdmin(admin.ModelAdmin):
    readonly_fields  = ['created_at']
    list_display = ['client', 'full_name', 'phone', 'email', 'topic', 'source', 'created_at']


@admin.register(VoiceAssignment)
class VoiceAssignmentAdmin(admin.ModelAdmin):
    list_display = ['voice', 'employee', 'assigned_at', 'additional_info']
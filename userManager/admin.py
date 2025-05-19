from django.contrib import admin

from .models import CustomUser, ScheduleWork, ScheduleRecord, Profile

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
# admin.site.register(ScheduleWork)
# admin.site.register(ScheduleRecord)

@admin.register(ScheduleWork)
class ScheduleWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduleWork._meta.get_fields()]

@admin.register(ScheduleRecord)
class ScheduleRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduleRecord._meta.get_fields()]
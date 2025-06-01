from datetime import datetime

from django.contrib import admin

from .models import CustomUser, ScheduleWork, ScheduleRecord, Profile
from .forms import ScheduleWorkForm
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)


# admin.site.register(ScheduleWork)
# admin.site.register(ScheduleRecord)


@admin.register(ScheduleWork)
class ScheduleWorkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduleWork._meta.get_fields()]
    form = ScheduleWorkForm

    def save_model(self, request, obj, form, change):
        dates = form.cleaned_data.get('dates')
        if dates:
            date_list = [date.strip() for date in dates.split(',')]
            for date in date_list:
                try:
                    date_object = datetime.strptime(date, '%d.%m.%Y')
                    schedule_work_instance, created = ScheduleWork.objects.get_or_create(
                        user=obj.user,
                        date=date_object
                    )
                except ValueError:
                    self.message_user(request, f'Ошибка формата даты: {date}', level='error')
        else:
            self.message_user(request, 'Поле дат не может быть пустым.', level='error')
    class Media:
        css = {
            'screen': (
                'multidatespicker.css',
            ),
        }
        js = (
            'JQ.js',
            'jquery-ui.js',
            'multidatespicker.js',
            'multi_dates_picker_init.js',
        )




@admin.register(ScheduleRecord)
class ScheduleRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ScheduleRecord._meta.get_fields()]

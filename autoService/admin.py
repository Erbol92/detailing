from django.contrib import admin

from .models import Auto, ModelAuto, Mark, GroupService, Service, PriceService

# Register your models here.
admin.site.register(ModelAuto)
admin.site.register(Mark)
admin.site.register(GroupService)

@admin.register(Auto)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Auto._meta.get_fields()]
    # list_editable = ['mark']
    # list_filter = ['category']
    search_fields = ['mark',]

@admin.register(PriceService)
class PriceServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PriceService._meta.get_fields()]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title','description','group',]

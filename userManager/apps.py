from django.apps import AppConfig



class UsermanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userManager'

    def ready(self):
        from django.contrib.auth.models import Group
        # Создание групп
        roles = ['Директор', 'Администратор', 'Мастер', 'Менеджер']
        for role in roles:
            Group.objects.get_or_create(name=role)

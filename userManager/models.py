from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class CustomUser(AbstractUser):
    inn = models.PositiveIntegerField('ИНН', blank=True, null=True, unique=True)
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name='пользователь', on_delete=models.CASCADE, related_name='user_profile')
    address = models.CharField('адрес', max_length=150,)
    phone = models.CharField('телефон', max_length=30)


    def __str__(self):
        return f'профиль {self.user} '

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

class ScheduleRecord(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Мастер', on_delete=models.CASCADE, related_name='records')
    client = models.ForeignKey('CustomUser', verbose_name='Клиент', on_delete=models.CASCADE, related_name='client_records')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    service = models.ForeignKey('autoService.Service', verbose_name='Услуга', on_delete=models.CASCADE, related_name='services_record')
    auto = models.ForeignKey('autoService.Auto', verbose_name='авто', on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('in_progress', 'Принято в работу'),
        ('ready_for_pickup', 'Можно забирать'),
        ('closed', 'Закрыт'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Состояние')
    
    def __str__(self):
        return f'мастер {self.user}'

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        ordering = ['date','start_time']

class ScheduleWork(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='Мастер', on_delete=models.CASCADE, related_name='work_times')
    date = models.DateField()

    def __str__(self):
        return f'мастер {self.user}'

    class Meta:
        verbose_name = 'рабочие дни'
        verbose_name_plural = 'рабочие дни'
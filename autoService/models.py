# from django.contrib.auth.models import User
from django.db import models
from userManager.models import CustomUser


# Create your models here.


class Mark(models.Model):
    title = models.CharField('название марки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'марка'
        verbose_name_plural = 'марки'


class ModelAuto(models.Model):
    title = models.CharField('название модели', unique=True)
    model_auto = models.ForeignKey(Mark, verbose_name='модель', on_delete=models.CASCADE,
                                   related_name='models_auto')

    def __str__(self):
        return f'{self.model_auto} {self.title}'

    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'модели'


class Auto(models.Model):
    mark = models.ForeignKey(Mark, verbose_name='марка авто', on_delete=models.CASCADE, related_name='marks')
    model = models.ForeignKey(ModelAuto, verbose_name='модель авто', on_delete=models.CASCADE, related_name='autos')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    vin = models.CharField(max_length=17, unique=True, verbose_name='VIN номер')
    auto_number = models.CharField(max_length=50, verbose_name='№ автомобиля', unique=True)
    user = models.ForeignKey(CustomUser, verbose_name='владелец', on_delete=models.CASCADE, related_name='autos',
                             null=True,
                             blank=True)

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return f"{self.mark} {self.year}"


class GroupService(models.Model):
    title = models.CharField('группа услуг', max_length=100)

    class Meta:
        verbose_name = 'Группа услуг'
        verbose_name_plural = 'Группа услуг'

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField('название услуги', max_length=100)
    description = models.TextField('описание')
    group = models.ForeignKey(GroupService, verbose_name='группа', on_delete=models.CASCADE)
    user = models.ManyToManyField(CustomUser, verbose_name='Мастера', related_name='services')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class PriceService(models.Model):
    CHOICES = [
        ("light", "легкий"),
        ("medium", "средний"),
        ("heavy", "тяжелый"),
    ]
    auto_body = models.CharField(max_length=10, choices=CHOICES, default='light')
    price = models.PositiveIntegerField('стоимость услуги', default=0)
    service = models.ForeignKey(Service, verbose_name='услуга', on_delete=models.CASCADE, related_name='service_prices')

    class Meta:
        verbose_name = 'Цена услуги'
        verbose_name_plural = 'Цена услуг'

    def __str__(self):
        return f'{self.service} {self.price}'



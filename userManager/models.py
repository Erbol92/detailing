from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    inn = models.PositiveIntegerField('ИНН', blank=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name='пользователь', on_delete=models.CASCADE, related_name='user_profile')
    address = models.CharField('адрес', max_length=150,)
    phone = models.CharField('телефон', max_length=30)


    def __str__(self):
        return f'профиль {self.user} '

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

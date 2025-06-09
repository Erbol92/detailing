from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from userManager.models import CustomUser


class Topic(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'тема заявки'
        verbose_name_plural = 'темы заявки'

    def __str__(self):
        return f'{self.title}'


class Voice(models.Model):
    client = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL,
                               verbose_name='зарег. клиент')
    full_name = models.CharField(max_length=255, blank=True, verbose_name='ФИО')
    phone = models.CharField('телефон', max_length=30, blank=True)
    email = models.EmailField('почта', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время обращения')
    topic = models.ForeignKey(Topic, verbose_name='тематика', on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=50, choices=[
        ('instagram', 'Instagram'),
        ('call', 'звонок'),
        ('vk', 'ВК'),
        ('tg', 'телеграм'),
        ('whatsapp', 'WhatsApp'),
    ], verbose_name='откуда заявка')
    status = models.BooleanField('Статус', default=False)

    def clean(self):
        # Убедитесь, что либо client, либо full_name заполнены
        if not self.client and not self.full_name:
            raise ValidationError('Укажите либо клиента, либо ФИО.')

    def get_absolute_url(self):
        return reverse('voice_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'

    def __str__(self):
        return f'{self.full_name if self.full_name else self.client} {self.created_at.date()}'


class VoiceAssignment(models.Model):
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='assignments', verbose_name='Заявка')
    employee = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Сотрудник')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')
    additional_info = models.TextField(blank=True, verbose_name='Доп. инфо')

    class Meta:
        verbose_name = 'История назначения'
        verbose_name_plural = 'История назначений'

    def __str__(self):
        return f'Заявка: {self.voice}, Сотрудник: {self.employee}, Дата: {self.assigned_at}'

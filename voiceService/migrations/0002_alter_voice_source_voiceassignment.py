# Generated by Django 5.2.1 on 2025-06-01 08:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voiceService', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='voice',
            name='source',
            field=models.CharField(choices=[('instagram', 'Instagram'), ('call', 'звонок'), ('vk', 'ВК'), ('tg', 'телеграм'), ('whatsapp', 'WhatsApp')], max_length=50, verbose_name='откуда заявка'),
        ),
        migrations.CreateModel(
            name='VoiceAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата назначения')),
                ('additional_info', models.TextField(blank=True, verbose_name='Маршрут')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='voiceService.voice', verbose_name='Заявка')),
            ],
            options={
                'verbose_name': 'История назначения',
                'verbose_name_plural': 'История назначений',
            },
        ),
    ]

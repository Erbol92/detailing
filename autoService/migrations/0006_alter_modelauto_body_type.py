# Generated by Django 5.2.1 on 2025-06-14 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoService', '0005_modelauto_body_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelauto',
            name='body_type',
            field=models.CharField(choices=[('light', 'легкий'), ('medium', 'средний'), ('heavy', 'тяжелый')], default='light', max_length=20, verbose_name='тип кузова'),
        ),
    ]

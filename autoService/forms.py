from django import forms
from .models import Auto, ModelAuto
from userManager.models import CustomUser


class AutoForm(forms.ModelForm):

    class Meta:
        model = Auto
        exclude = ['user',]


class ClientListForm(forms.Form):
    client = forms.ModelChoiceField(
        label='клиент',
        queryset=CustomUser.objects.exclude(is_staff=True),  # Исключаем мастеров с is_staff=True
        empty_label="Выберите клиента",  # Текст для пустого значения
        required=True  # Укажите, что поле обязательно для заполнения
    )
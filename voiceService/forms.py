from django import forms
from userManager.models import CustomUser

from .models import Voice, VoiceAssignment


class VoicenForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        label='клиент',
        queryset=CustomUser.objects.filter(is_staff=False),  # Исключаем мастеров с is_staff=True
        empty_label="Выберите клиента",  # Текст для пустого значения
        required=False  # Укажите, что поле обязательно для заполнения
    )

    class Meta:
        model = Voice
        exclude = ['status']

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        full_name = cleaned_data.get('full_name')

        if not client and not full_name:
            raise forms.ValidationError('Укажите либо клиента, либо ФИО.')


class VoiceAssignmentForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        label='сотрудник',
        queryset=CustomUser.objects.filter(is_staff=True),  # Исключаем мастеров с is_staff=True
        empty_label="Выберите сотрудника",  # Текст для пустого значения
        required=True  # Укажите, что поле обязательно для заполнения
    )
    class Meta:
        model = VoiceAssignment
        exclude = ['voice']

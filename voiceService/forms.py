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

class VoiceUserForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        label='клиент',
        queryset=CustomUser.objects.filter(is_staff=False),
        empty_label="Выберите клиента",
        required=False
    )
    
    class Meta:
        model = Voice
        exclude = ['status','source']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из аргументов
        super(VoiceUserForm, self).__init__(*args, **kwargs)
        print()
        self.fields.pop('client', None)
        self.fields.pop('status', None)
        if user and user.is_authenticated:
            # Если пользователь авторизован, оставляем поля client, full_name и status
            self.fields.pop('full_name', None)
            self.fields['phone'].initial = user.user_profile.phone
            self.fields['email'].initial = user.email
        else:
            # Если пользователь не авторизован, удаляем поля client и status
            self.fields['phone'].required = True
            self.fields['email'].required = True
            self.fields['full_name'].required = True

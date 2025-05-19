from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from .models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone']


class LegalEntity(UserCreationForm):
    inn = forms.IntegerField(label='ИНН', min_value=1000000000, max_value=9999999999)

    class Meta:
        model = CustomUser
        fields = ['username', 'inn', 'email', 'password1', 'password2']

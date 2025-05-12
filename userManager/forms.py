from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email','inn']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone']


class LegalEntity(UserCreationForm):
    inn = forms.IntegerField(label='ИНН', min_value=1000000000, max_value=9999999999)


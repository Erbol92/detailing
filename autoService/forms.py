from django import forms
from .models import Auto, ModelAuto


class AutoForm(forms.ModelForm):

    class Meta:
        model = Auto
        exclude = ['user',]


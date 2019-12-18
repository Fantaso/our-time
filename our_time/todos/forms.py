from django import forms
from django.utils import timezone

from .models import Task


class DateForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(
        attrs={
            'type': 'date',
            'value': timezone.now().strftime('%Y-%m-%d'),
        }
    ))

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ('deadline',)  # if included, first it needs to retrieve correct format

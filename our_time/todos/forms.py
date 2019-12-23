from django import forms
from django.utils import timezone

from .models import Task


class DateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'is_done': forms.CheckboxInput(attrs={'class': 'checkbox', 'type': 'checkbox'}),
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'rows': '10', 'class': 'textarea'}),
            'priority': forms.Select(attrs={'class': 'select'}),
            'deadline': forms.DateInput(
                attrs={'class': 'input', 'type': 'date', 'value': timezone.now().strftime('%Y-%m-%d')},
                format='%Y-%m-%d')
            ,
        }

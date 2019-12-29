from django import forms

from .models import Book


# this form could be decouple and reused for also the model of the book in BookForm
class ISBNForm(forms.Form):
    isbn = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Write the ISBN-10 code here...'}
    ))


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            # TOOD: this definetly needs a refactor
            'isbn_10': forms.TextInput(attrs={'class': 'input'}),
            'isbn_13': forms.TextInput(attrs={'class': 'input'}),
            'title': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'rows': '10', 'class': 'textarea'}),
            'publish_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}, format='%Y-%m-%d'),
            'authors': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'buy_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            'holder': forms.TextInput(attrs={'class': 'input'}),
            'image': forms.FileInput(attrs={'class': 'file-input'}),
            'pages_num': forms.TextInput(attrs={'class': 'input'}),
            'publishers': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'genres': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'languages': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
        }

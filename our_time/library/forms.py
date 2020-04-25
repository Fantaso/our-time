from django import forms

from .models import Book, Author, Publisher, Genre, Language


# this form could be decouple and reused for also the model of the book in BookForm
class ISBNForm(forms.Form):
    isbn = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'Write the ISBN-10 code here...'}
    ))


# class OpenLibrarySerializer(forms.Form):
#     isbn_10= forms.CharField()
#     title= forms.CharField()
#     description= forms.CharField()
#     publish_date= forms.DateField()
#     cover= forms.ImageField(required=False)
#     number_of_pages= forms.IntegerField()
#     authors= forms.SelectMultiple()
class BookForm(forms.ModelForm):
    # authors = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ()
        widgets = {
            # TOOD: this definetly needs a refactor
            # 'owner': forms.Select(attrs={'class': 'select'}),
            'isbn_10': forms.TextInput(attrs={'class': 'input'}),
            # 'isbn_13': forms.TextInput(attrs={'class': 'input'}),
            'title': forms.TextInput(attrs={'class': 'input'}),
            'subtitle': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'rows': '10', 'class': 'textarea'}),
            'publish_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}, format='%Y-%m-%d'),

            # 'buy_date': forms.DateInput(attrs={'class': 'input', 'type': 'date'}),
            # 'holder': forms.TextInput(attrs={'class': 'input'}),
            'cover': forms.FileInput(attrs={'class': 'file-input'}),
            'number_of_pages': forms.TextInput(attrs={'class': 'input'}),

            'authors': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'publishers': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'genres': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
            'languages': forms.SelectMultiple(attrs={'class': 'select is-multiple', 'size': '3'}),
        }


class OpenLibraryBookForm(forms.ModelForm):
    # authors = forms.ModelChoiceField(queryset=Author.objects.all(), required=False)
    class Meta:
        model = Book
        fields = (
            'owner',
            'isbn_10',
            'title',
            'subtitle',
            'description',
            'publish_date',
            'number_of_pages',

            'cover',

            # 'authors',
            # 'publishers',
            # 'genres',
            # 'languages',
            # 'characters',
        )

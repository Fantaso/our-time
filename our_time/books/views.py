from pprint import pprint

import requests
from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView, DeleteView, UpdateView,
    ListView, DetailView, FormView,
)

#######################
###     BOOK        ###
#######################
from .forms import BookForm
# consider using reverse_lazy() here as class attrs are evaluated on file import
# or on get_sucess_url() with reverse() as functions are not evaluated on import
from .forms import ISBNForm
from .models import Author, Book
from .services import get_book_data


class BookList(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'


class BookDetail(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class BookCreate(CreateView):
    model = Book
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book-list')
    form_class = BookForm
    success_message = '%(title)s was created successfully'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data

    ######
    ## All this was to received context data and prepopulate the form
    ######
    # def get_initial(self):
    #     """
    #     Prepopulate the create view and
    #     return the initial data to use for forms on this view.
    #     """
    #     initial = super().get_initial()
    #     # kwargs = super().get_context_data()
    #     # print(kwargs)
    #     initial['title'] = 'Don Quijote'
    #     return initial

    # def get_context_data(self, **kwargs):
    #     """Insert the form into the context dict."""
    #
    #     print('KWARGS: ', kwargs)
    #     if kwargs.get('isbn'):
    #         print(kwargs.get('isbn'))
    #         pass
    #
    #     ctx = super().get_context_data(**kwargs)
    #     form = ctx.get('form')
    #     return ctx


class BookUpdate(UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    # if successurlno specified. takes you to detail view
    # success_url = reverse_lazy('books:book-list')
    form_class = BookForm

    def form_valid(self, form):
        print(form.data)
        """The for is already valid so add flash message and keep rolling the MRO."""
        messages.success(self.request, f'Book update successfully: {self.object.title}.')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print('################# get_form_kwargs ############')
        print(kwargs.get('data'), end='\n\n')
        print(kwargs.get('files'))
        print('################# get_form_kwargs ############')
        return kwargs

    # # FormMixin
    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = {
    #         'initial': self.get_initial(),
    #         'prefix': self.get_prefix(),
    #     }
    #
    #     if self.request.method in ('POST', 'PUT'):
    #         print()
    #         kwargs.update({
    #             'data': self.request.POST,
    #             'files': self.request.FILES,
    #         })
    #     return kwargs
    #
    # # ModelFormMixin
    # def get_form_kwargs(self):
    #     """Return the keyword arguments for instantiating the form."""
    #     kwargs = super().get_form_kwargs()
    #     if hasattr(self, 'object'):
    #         kwargs.update({'instance': self.object})
    #     return kwargs


class BookDelete(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book-list')
    context_object_name = 'book'

    def delete(self, request, *args, **kwargs):
        """Deleting through the inherited delete method and adding a flash message and keep rolling MRO."""
        messages.success(request, f'Book deleted successfully: {self.get_object().title}.')
        return super().delete(request, *args, **kwargs)


class FetchBookData(FormView):
    template_name = 'books/isbn.html'
    form_class = ISBNForm
    success_url = 'books:book-list'

    def form_valid(self, form):
        """
        Receives the ISBN of the book to query the books API
        and save the validate book data into the database and
        redirects the user to the update view to confirm the data
        fetch from the 3rd-party API.
        """

        isbn = form.cleaned_data.get('isbn')

        ## BOOK
        ## GET DATA FROM API
        raw_data = get_book_data(isbn)
        ### ISBN DO NOT EXIST
        if not raw_data:
            messages.add_message(self.request, messages.INFO,
                                 f"ISBN:{isbn} - ISBN code doesn't exist in openlibrary.org")
            print('### Book dont exist ###')
            return HttpResponseRedirect(reverse('books:isbn'))

        valido = {'title': 'The Little Prince', 'description': '', 'publish_date': None, 'authors': '<QuerySet[] >',
                  'image': '< SimpleUploadedFile: The Little Prince0156012197.jpg(image / jpeg) >', 'buy_date': None,
                  'holder': ''}
        print(raw_data)
        ## SERIALIZE DATA
        book_dict = raw_data.get(f'ISBN:{isbn}', {})
        image_url = book_dict.get('cover', {}).get('large')

        title = book_dict.get('title')
        # author = book_dict.get('authors')[0]['name']  # just grabing the first one to test
        publish_date = book_dict.get('publish_date')
        # add all data to be saved in db. image is appended in a different dict file_data
        data = dict(isbn_10=isbn, title=title)
        print('######################################')
        print('Publish Date, Title, ImageURL, Book')
        print(publish_date, title, image_url, book_dict)
        print('######################################')
        print('RAW DATA')
        pprint(raw_data)
        print('######################################')
        print('######################################')

        ### FILE HANDLING
        import os
        from urllib.parse import urlparse
        # work the image around
        form = None
        if image_url:
            parser = urlparse(image_url).path
            image_name = os.path.basename(parser)  # this changes for the name of the book and so on
            image_ext = os.path.splitext(image_name)[1]

            # download and save image file in filesystem
            image_bin = requests.get(image_url)
            image_filename = os.path.join(settings.MEDIA_ROOT, 'books_cover', title + isbn + image_ext)
            with open(image_filename, 'wb') as image:
                image.write(image_bin.content)
            # read file from filesystem
            image = open(image_filename, 'rb')
            # organized vaiadted data
            file_data = {'image': SimpleUploadedFile(image_filename, image.read())}
            form = BookForm(data=data, files=file_data)
        ## VALIDATE DATA
        # i need to add the author first if not yet in db. :s
        if not form:
            form = BookForm(data=data)

        if form.is_valid():
            messages.add_message(self.request, messages.SUCCESS, f"ISBN:{isbn} - And books' title is '{title}'")
            print(form.cleaned_data)
            book_obj = form.save()
            return HttpResponseRedirect(reverse('books:book-update', args=[int(book_obj.id)]))

        # add here the errors and soon as messages
        # print(form.is_valid())
        print(form.data)
        # print(form.validate_unique())
        # print(form.errors)
        # print(form.changed_data)
        # print(form.clean())
        # print(form.cleaned_data.get('title'))
        print(form.cleaned_data)

        messages.add_message(self.request, messages.ERROR, f"ISBN:{isbn} - {str(form.cleaned_data)}")
        return HttpResponseRedirect(reverse('books:isbn'))


#######################
###     AUTHOR      ###
#######################
class AuthorList(ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'author_list'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'books/author_detail.html'


class AuthorCreate(CreateView):
    model = Author
    template_name = 'books/author_create.html'
    success_url = reverse_lazy('books:author-list')
    fields = '__all__'
    success_message = '%(first_name)s was created successfully'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class AuthorUpdate(UpdateView):
    model = Author
    template_name = 'books/author_update.html'
    success_url = reverse_lazy('books:author-list')
    fields = '__all__'

    def form_valid(self, form):
        """The for is already valid so add flash message and keep rolling the MRO."""
        messages.success(self.request, f'Author update successfully: {self.object.full_name}.')
        return super().form_valid(form)


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'books/author_delete.html'
    success_url = reverse_lazy('books:author-list')
    context_object_name = 'author'

    def delete(self, request, *args, **kwargs):
        """Deleting through the inherited delete method and adding a flash message and keep rolling MRO."""
        messages.success(request, f'Author deleted successfully: {self.get_object().full_name}.')
        return super().delete(request, *args, **kwargs)

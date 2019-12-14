from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, UpdateView, ListView, DetailView
)

# consider using reverse_lazy() here as class attrs are evaluated on file import
# or on get_sucess_url() with reverse() as functions are not evaluated on import
from .models import Author, Book


class BookList(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'


class BookCreate(SuccessMessageMixin, CreateView):
    model = Book
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book-list')
    fields = '__all__'
    success_message = '%(title)s was created successfully'


class BookDetail(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class BookUpdate(UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('books:book-list')
    fields = '__all__'

    def form_valid(self, form):
        """The for is already valid so add flash message and keep rolling the mro."""
        # add sucessfull message
        messages.success(self.request, f'Book update successfully: {self.object.title}.')
        return super().form_valid(form)


class BookDelete(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book-list')
    context_object_name = 'book'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        # add sucessfull message
        messages.success(self.request, f'Book deleted successfully: {self.object.title}.')

        self.object.delete()
        return HttpResponseRedirect(success_url)


####################################3

class AuthorList(ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'author_list'


class AuthorCreate(CreateView):
    model = Author
    template_name = 'books/author_create.html'
    success_url = reverse_lazy('books:author-list')
    fields = '__all__'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'books/author_detail.html'


class AuthorUpdate(UpdateView):
    model = Author
    template_name = 'books/author_update.html'
    success_url = reverse_lazy('books:author-list')
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'books/author_delete.html'
    success_url = reverse_lazy('books:list')
    context_object_name = 'author'

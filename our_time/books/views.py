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


#######################
###     BOOK        ###
#######################
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
    fields = '__all__'
    success_message = '%(title)s was created successfully'

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class BookUpdate(UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('books:book-list')
    fields = '__all__'

    def form_valid(self, form):
        """The for is already valid so add flash message and keep rolling the MRO."""
        messages.success(self.request, f'Book update successfully: {self.object.title}.')
        return super().form_valid(form)


class BookDelete(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:book-list')
    context_object_name = 'book'

    def delete(self, request, *args, **kwargs):
        """Deleting through the inherited delete method and adding a flash message and keep rolling MRO."""
        messages.success(request, f'Author deleted successfully: {self.get_object().full_name}.')
        return super().delete(request, *args, **kwargs)


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

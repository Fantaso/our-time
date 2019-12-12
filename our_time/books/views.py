from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

# consider using reverse_lazy() here as class attrs are evaluated on file import
# or on get_sucess_url() with reverse() as functions are not evaluated on import
from .models import Author, Book


class BookList(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'


class BookCreate(CreateView):
    model = Book
    template_name = 'books/book_create.html'
    success_url = reverse_lazy('books:book-list')
    fields = '__all__'


class BookDetail(DetailView):
    model = Book
    template_name = 'books/book_detail.html'


class BookUpdate(UpdateView):
    model = Book
    template_name = 'books/book_update.html'
    success_url = reverse_lazy('books:book-list')
    fields = '__all__'


class BookDelete(DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books:list')
    context_object_name = 'book'

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


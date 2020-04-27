from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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
from .openlibrary_api.manager import OpenLibraryManager
from .tasks import delayed_find_book_and_save


class BookBase:
    model = Book


class BookList(LoginRequiredMixin, BookBase, ListView):
    template_name = 'library/books/list.html'
    context_object_name = 'book_list'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user).all()


class BookDetail(BookBase, DetailView):
    template_name = 'library/books/detail.html'


class BookCreate(BookBase, CreateView):
    template_name = 'library/books/create.html'
    success_url = reverse_lazy('library:book-list')
    form_class = BookForm
    success_message = '%(title)s was created successfully'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


class BookUpdate(BookBase, UpdateView):
    template_name = 'library/books/update.html'
    form_class = BookForm

    def form_valid(self, form):
        print(form.data)
        """The for is already valid so add flash message and keep rolling the MRO."""
        messages.success(self.request, f'Book update successfully: {self.object.title}.')
        return super().form_valid(form)


class BookDelete(BookBase, DeleteView):
    template_name = 'library/books/delete.html'
    success_url = reverse_lazy('library:book-list')
    context_object_name = 'book'

    def delete(self, request, *args, **kwargs):
        """Deleting through the inherited delete method and adding a flash message and keep rolling MRO."""
        messages.success(request, f'Book deleted successfully: {self.get_object().title}.')
        return super().delete(request, *args, **kwargs)


class FetchBookData(FormView):
    template_name = 'library/books/isbn.html'
    form_class = ISBNForm
    success_url = reverse_lazy('library:book-list')

    def form_valid(self, form):
        """
        Receives the ISBN of the book to be queried.
        checks if the books exists to alert user right away
        and execute the task of finding and saving the book in database.
        """
        isbn = form.cleaned_data.get('isbn')

        if not OpenLibraryManager.book_exists('isbn', isbn):
            messages.info(self.request, f"ISBN:{isbn} - ISBN code doesn't exist in openlibrary.org")
            return super().form_invalid(form)

        messages.success(self.request, f"Book isbn:{isbn} will be added to your list.")
        delayed_find_book_and_save(self.request.user, isbn)
        return super().form_valid(form)


#######################
###     AUTHOR      ###
#######################
class AuthorList(ListView):
    model = Author
    template_name = 'library/authors/list.html'
    context_object_name = 'author_list'


class AuthorDetail(DetailView):
    model = Author
    template_name = 'library/authors/detail.html'


class AuthorCreate(CreateView):
    model = Author
    template_name = 'library/authors/create.html'
    success_url = reverse_lazy('library:author-list')
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
    template_name = 'library/authors/update.html'
    success_url = reverse_lazy('library:author-list')
    fields = '__all__'

    def form_valid(self, form):
        """The for is already valid so add flash message and keep rolling the MRO."""
        messages.success(self.request, f'Author update successfully: {self.object.full_name}.')
        return super().form_valid(form)


class AuthorDelete(DeleteView):
    model = Author
    template_name = 'library/authors/delete.html'
    success_url = reverse_lazy('library:author-list')
    context_object_name = 'author'

    def delete(self, request, *args, **kwargs):
        """Deleting through the inherited delete method and adding a flash message and keep rolling MRO."""
        messages.success(request, f'Author deleted successfully: {self.get_object().full_name}.')
        return super().delete(request, *args, **kwargs)

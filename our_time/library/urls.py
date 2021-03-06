from django.urls import path

from .views import BookList, BookCreate, BookDetail, BookUpdate, BookDelete, AuthorList, AuthorCreate, \
    AuthorDetail, AuthorUpdate, AuthorDelete, FetchBookData

app_name = 'library'
urlpatterns = [
    # BOOKS
    # crudl
    path('books/', BookList.as_view(), name='book-list'),
    path('create-book/', BookCreate.as_view(), name='book-create'),
    path('<int:pk>/book', BookDetail.as_view(), name='book-detail'),
    path('<int:pk>/update-book', BookUpdate.as_view(), name='book-update'),
    path('<int:pk>/delete-book', BookDelete.as_view(), name='book-delete'),
    # services
    path('isbn/', FetchBookData.as_view(), name='book-isbn'),

    # AUTHOR
    # crudl
    path('authors/', AuthorList.as_view(), name='author-list'),
    path('create-author/', AuthorCreate.as_view(), name='author-create'),
    path('<int:pk>/author', AuthorDetail.as_view(), name='author-detail'),
    path('<int:pk>/update-author', AuthorUpdate.as_view(), name='author-update'),
    path('<int:pk>/delete-author', AuthorDelete.as_view(), name='author-delete'),
]

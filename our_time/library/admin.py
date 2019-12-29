from django.contrib import admin

from .models import Book, Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_filter = ('last_name', 'first_name', 'birthdate')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display = ('__all__',)
    list_filter = ('title', 'publish_date')
    # search_fields = ('first_name', 'last_name')

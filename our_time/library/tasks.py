from pprint import pprint

from .forms import OpenLibraryBookForm
from .models import Author, Publisher, Genre, Character


# def book_exists(isbn):
#     from .openlibrary.manager import OpenLibraryManager
#     manager = OpenLibraryManager()
#     json_data = manager.find_book('isbn', isbn)
#     if json_data:
#         return True
#     return False


def delayed_find_book_and_save(user, isbn: str = None):
    from .openlibrary_api.manager import OpenLibraryManager, ImageManager

    if not isbn:
        return 'ISBN not provided.'

    manager = OpenLibraryManager()
    img_manager = ImageManager()
    json_data = manager.find_book('isbn', isbn)

    # {testing}
    # pprint(manager.find_book('olid', 'OL13101191W')) # alicein wonder not found
    # pprint(manager.find_book('olid', 'OL24173027M'))  # another version alice in wonderland
    pprint(manager.find_book('olid', 'OL24286565M'))  # olid from isbn search
    pprint(manager.find_book('olid', 'OL9173430M'))  # from olid website page
    pprint(json_data)
    # {end testing}

    if not json_data:
        return f"ISBN:{isbn} - ISBN not found in openlibrary.org"

    # get formatted book data and create the form with ir
    book_data = manager.parse_book(json_data)

    authors = book_data.pop('authors')
    publishers = book_data.pop('publishers')
    genres = book_data.pop('genres')
    characters = book_data.pop('characters')

    book_form = OpenLibraryBookForm(data=book_data)

    # add image to the form to be saved.
    image_data = img_manager.get_django_upload_image_data(book_data.get('cover'))
    if image_data:
        book_form.files = image_data

    # book form validation
    if book_form.is_valid():
        book = book_form.save()
        book.owner = user

        # check relationships
        if authors:
            # replcaing list of names for db objtects
            # TODO: if get or create save the obj already, the author creation can be reduced to a comprenhension
            # authors_obj = [Author.objects.get_or_create(name=author) for author in authors]
            for author in authors:
                author_db, _ = Author.objects.get_or_create(name=author)
                author_db.save()
                book.authors.add(author_db)
                book.save()
        if publishers:
            for publisher in publishers:
                publisher_db, _ = Publisher.objects.get_or_create(name=publisher)
                publisher_db.save()
                book.publishers.add(publisher_db)
                book.save()
        if genres:
            for genre in genres:
                genre_db, _ = Genre.objects.get_or_create(name=genre)
                genre_db.save()
                book.genres.add(genre_db)
                book.save()

        if characters:
            for character in characters:
                character_db, _ = Character.objects.get_or_create(name=character)
                character_db.save()
                book.characters.add(character_db)
                book.save()
        return f"Book added {book} ISBN:{book.isbn_10} - And books' title is '{book.title}'"
    else:
        print(book_form.errors)
        return f"ISBN:{isbn} - {str(book_form.errors)}"

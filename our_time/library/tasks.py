from pprint import pprint

from .forms import OpenLibraryBookForm
from .models import Author, Publisher, Genre, Character


def get_or_create_m2m(str_list, model):
    """
    Receives a list of names
    Finds each in the database if not it creates it
    Return a list of db instances.
    """
    if str_list:
        instance_list = []
        # instances = [model.objects.get_or_create(name=_str) for _str in str_list]
        for _str in str_list:
            instance, _ = model.objects.get_or_create(name=_str)
            instance.save()
            instance_list.append(instance)
        return instance_list
    return []


def delayed_find_book_and_save(user, isbn: str = None):
    from .openlibrary_api.manager import OpenLibraryManager, ImageManager

    if not isbn:
        return 'ISBN not provided.'

    manager = OpenLibraryManager()
    img_manager = ImageManager()
    json_data = manager.find_book('isbn', isbn)

    # {testing}
    print('[##  DATA  ##]')
    pprint(json_data)
    # pprint(manager.find_book('olid', 'OL13101191W')) # alicein wonder not found
    # pprint(manager.find_book('olid', 'OL24173027M'))  # another version alice in wonderland
    # pprint(manager.find_book('olid', 'OL24286565M'))  # olid from isbn search
    # pprint(manager.find_book('olid', 'OL9173430M'))  # from olid website page
    print('[##  DETAILS  ##]')
    pprint(manager.find_book('isbn', isbn, jscmd='details'))  # from olid website page
    # {end testing}

    if not json_data:
        return f"ISBN:{isbn} - ISBN not found in openlibrary.org"

    # get formatted book data and create the form with ir
    book_data = manager.parse_book(json_data)

    # get all relationships before saving it in form
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
        book_form.instance.owner = user
        book = book_form.save()

        # process all relationships and add them to the book instance
        book.authors.add(*get_or_create_m2m(authors, Author))
        book.publishers.add(*get_or_create_m2m(publishers, Publisher))
        book.genres.add(*get_or_create_m2m(genres, Genre))
        book.characters.add(*get_or_create_m2m(characters, Character))

        # save the book with all relationships
        book.save()
        return f"Book added {book} ISBN:{book.isbn_10} - And books' title is '{book.title}'"
    else:
        print(book_form.errors)
        return f"ISBN:{isbn} - {str(book_form.errors)}"

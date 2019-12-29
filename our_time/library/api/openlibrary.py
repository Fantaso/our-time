import requests
from urllib.parse import urljoin


class MainApi:
    """
    This will handle the requests to the openlibrary.org.
    It will be used to retrieve data information base on the ISBN.
    """
    _base_url = 'http://openlibrary.org/api/'
    _books_url = urljoin(_base_url, 'books')

    # ?bibkeys=ISBN:9780241347768&format=json&jscmd=data

    @classmethod
    def main(cls, isbn):
        if not isbn:
            return 'No ISBN given!'

        # get the book data with the ISBN
        book = cls.get_book_data(isbn)

        # serialize the data and handle validation
        # save the data into the db

    @classmethod
    def get_book_data(cls, isbn):
        params = {
            'bibkeys': f'ISBN:{isbn}',
            'jscmd': 'data',  # data: gets data about book, viewapi: gets html pages
            'format': 'json',  # api by default returns js unless specified
        }
        return requests.get(cls._books_url, params=params).json()


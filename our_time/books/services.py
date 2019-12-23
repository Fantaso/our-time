import requests


def get_book_data(isbn):
    books_url = 'http://openlibrary.org/api/books'
    params = {
        'bibkeys': f'ISBN:{isbn}',
        'jscmd': 'data',  # data: gets data about book, viewapi: gets html pages
        'format': 'json',  # api by default returns js unless specified
    }
    return requests.get(books_url, params=params).json()

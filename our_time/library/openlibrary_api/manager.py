import os
import uuid
from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from .parser import OpenLibraryParser


class OpenLibraryManager:
    """
    This will handle the requests to the openlibrary.org.
    It will be used to retrieve data information base on the ISBN.
    """
    # ?bibkeys=ISBN:9780241347768&format=json&jscmd=data

    books_url = 'http://openlibrary.org/api/books'
    params = ({
        'jscmd': 'data',  # data: gets data about book, viewapi: gets html pages, details: internal info abput the book
        'format': 'json',  # api by default returns js unless specified
    })
    _book = None
    _identifier = None

    _identifiers = ['isbn', 'olid', 'lccn', 'oclc']

    def find_book(self, identifier: str, book_code: str, jscmd=None):
        if jscmd:
            self.params.update(jscmd=jscmd)
        if identifier in self._identifiers:
            self._identifier = identifier
            # bibkeys: format openlibrary receives the isbn number to be searched
            self.params.update(bibkeys=f'{identifier.upper()}:{book_code}')
            # TODO: ConnectionError - Exception when no internet or failed connection.
            return requests.get(self.books_url, params=self.params).json()
        return None

    def parse_book(self, json_data):
        if json_data:
            parser = OpenLibraryParser(json_data)
            self._book = parser.to_dict()
            return self._book
        return None

    @staticmethod
    def book_exists(identifier: str, book_code: str):
        manager = OpenLibraryManager()
        if manager.find_book(identifier, book_code):
            return True
        return False


class ImageManager:
    def get_django_upload_image_data(self, image_url=None):
        image_url = image_url
        filepath = self.get_correct_file(image_url)
        if image_url:
            self.download_image(url=image_url, path=filepath)
            with open(filepath, 'rb') as image:
                image_data = {'cover': SimpleUploadedFile(filepath, image.read())}
            return image_data

    def download_image(self, url='', path='.'):
        # download and save image file in filesystem
        image_binaries = requests.get(url)
        with open(path, 'wb') as image:
            image.write(image_binaries.content)

    def get_correct_file(self, url):
        filename, fileext = self.extract_filename_and_ext(url)
        filepath = os.path.join(settings.MEDIA_ROOT, 'books_cover', f'{uuid.uuid4()}_{filename}')
        return filepath

    def extract_filename_and_ext(self, url):
        parser = urlparse(url).path
        name = os.path.basename(parser)  # this changes for the name of the book and so on
        ext = os.path.splitext(name)[1]
        return name, ext


'''
  return session.request(method=method, url=url, **kwargs)
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/sessions.py", line 533, in request
    resp = self.send(prep, **send_kwargs)
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/sessions.py", line 668, in send
    history = [resp for resp in gen] if allow_redirects else []
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/sessions.py", line 668, in <listcomp>
    history = [resp for resp in gen] if allow_redirects else []
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/sessions.py", line 247, in resolve_redirects
    **adapter_kwargs
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/sessions.py", line 646, in send
    r = adapter.send(request, **kwargs)
  File "/home/fantaso/.virtualenvs/our-time-together/lib/python3.6/site-packages/requests/adapters.py", line 498, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response',))

'''

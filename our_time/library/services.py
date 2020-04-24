# import requests
#
#
# class OpenLibraryParser:
#     url = 'http://openlibrary.org/books/OL24229110M/IT'
#
#     title = 'IT'
#     by_statement = 'Stephen King.'
#     publish_date = '1987-09'
#
#     number_of_pages = 1093
#     pagination = 'x, 1093 p. ;'
#
#     publishers = [{'name': 'New American Library'}]
#     authors = [{'name': 'Stephen King',
#                 'url': 'http://openlibrary.org/authors/OL2162284A/Stephen_King'}]
#
#     cover = {'large': 'https://covers.openlibrary.org/b/id/8569281-L.jpg',
#              'medium': 'https://covers.openlibrary.org/b/id/8569281-M.jpg',
#              'small': 'https://covers.openlibrary.org/b/id/8569281-S.jpg'}
#
#     notes = 'A Signet Book\r\nUS 4.95/CAN 5.95'
#     publish_places = [{'name': 'New York, N.Y., USA'}]
#     subject_people = [{'name': 'IT',
#                        'url': 'https://openlibrary.org/subjects/person:it'}]
#     subject_places = [{'name': 'Derry',
#                        'url': 'https://openlibrary.org/subjects/place:derry'}]
#     subject_times = [
#         {'name': '1957',
#          'url': 'https://openlibrary.org/subjects/time:1957'},
#         {'name': '1958',
#          'url': 'https://openlibrary.org/subjects/time:1958'}
#     ]
#     subjects = [
#         {'name': 'coming of age',
#          'url': 'https://openlibrary.org/subjects/coming_of_age'},
#         {'name': 'thrillers',
#          'url': 'https://openlibrary.org/subjects/thrillers'},
#         {'name': 'suspense',
#          'url': 'https://openlibrary.org/subjects/suspense'},
#         {'name': 'horror',
#          'url': 'https://openlibrary.org/subjects/horror'},
#         {'name': 'Schwinn bicycles',
#          'url': 'https://openlibrary.org/subjects/schwinn_bicycles'},
#         {'name': 'catatonia',
#          'url': 'https://openlibrary.org/subjects/catatonia'},
#         {'name': 'homosexuality',
#          'url': 'https://openlibrary.org/subjects/homosexuality'}
#     ]
#
#     def __init__(self, json_data):
#         self.isbn, self.book_data = (
#             self.extract_isbn_and_book(json_data)
#         )
#
#     def extract_isbn_and_book(self, json_data):
#         isbn, book = next(iter(json_data.items()))
#         isbn.replace('ISBN:', '').strip()
#         return isbn, book
#
#     def to_dict(self):
#         return dict(
#             title=self.parse_title(),
#             description=self.parse_description(),
#             publish_date=self.parse_publish_date(),
#             number_of_pages=self.parse_number_of_pages(),
#             authors=self.parse_authors(),
#             publishers=self.parse_publishers(),
#             genres=self.parse_genres(),
#             languages=self.parse_languages(),
#             cover=self.parse_cover(),
#         )
#
#     def parse_title(self):
#         return self.book_data.get('title', '')
#
#     def parse_description(self):
#         return self.book_data.get('notes', '')
#
#     def parse_publish_date(self):
#         publish_date = self.book_data.get('publish_date', '').strip()
#         from dateutil import parser
#
#         # grab the first year "1961-71"
#         if len(publish_date) == 6 and '-' in publish_date:
#             publish_date = publish_date.split('-')[0]
#
#         return parser.parse(publish_date)
#
#     def parse_number_of_pages(self):
#         return self.book_data.get('number_of_pages', '')
#
#     def parse_authors(self):
#         authors = self.book_data.get('authors', [])
#         return [author['name'] for author in authors]
#
#     def parse_publishers(self):
#         publishers = self.book_data.get('publishers', [])
#         return [publisher['name'] for publisher in publishers]
#
#     def parse_genres(self):
#         genres = self.book_data.get('genres', [])
#         return [genre['name'] for genre in genres]
#
#     def parse_languages(self):
#         return []
#
#     def parse_cover(self):
#         sizes = ['large', 'medium', 'small']
#         images = self.book_data.get('cover', {})
#
#         for size in sizes:
#             if size in images:
#                 return images[size]
#         else:
#             return ''
#
#
# class OpenLibraryManager:
#     books_url = 'http://openlibrary.org/api/books'
#     params = ({
#         'jscmd': 'data',  # data: gets data about book, viewapi: gets html pages
#         'format': 'json',  # api by default returns js unless specified
#     })
#     book = None
#     isbn = None
#
#     def find_book_by_isbn10(self, isbn: str):
#         # TODO: ConnectionError - Exception when no internet or failed connection.
#         self.isbn = isbn
#         self.params.update(bibkeys=f'ISBN:{isbn}')  # format openlibrary receives the isbn number to be searched
#         return requests.get(self.books_url, params=self.params).json()
#
#     def parse_book_by_isbn10(self, json_data):
#         parser = OpenLibraryParser(json_data)
#         self.book = parser.to_dict()
#         return self.book
#
#
#
#
# # isbn = front endfor process
# # LibraryOrg:
# # raw_book_data = scraping isbn process
# # model_ready_book_data
# # response: if success UpdateView else IsbnView
#
# # def download_image(self, url):
# #     def extract_filename_and_ext(url):
# #         import os
# #         from urllib.parse import urlparse
# #         parser = urlparse(url).path
# #         name = os.path.basename(parser)  # this changes for the name of the book and so on
# #         ext = os.path.splitext(name)[1]
# #         return name, ext
# #
# #     def get_correct_file(url):
# #         filename, fileext = extract_filename_and_ext(url)
# #         import os
# #         return os.path.join(settings.MEDIA_ROOT, 'books_cover', f'{self.isbn}_{filename}{fileext}')
# #
# #     # download and save image file in filesystem
# #     image_binaries = requests.get(url)
# #
# #     with open(get_correct_file(url), 'wb') as image:
# #         image.write(image_binaries.content)
# #     # read file from filesystem
# #     with open(get_correct_file(url), 'rb') as image:
# #             file_data = {'image': SimpleUploadedFile(get_correct_file(url), image.read())}
# #     form = BookForm(data=data, files=file_data)
#
# def get_book(api):
#     isbn = form.cleaned_data.get('isbn')
#
#     ## BOOK
#     ## GET DATA FROM API
#     raw_data = get_book_data(isbn)
#     ### ISBN DO NOT EXIST
#     if not raw_data:
#         messages.add_message(self.request, messages.INFO,
#                              f"ISBN:{isbn} - ISBN code doesn't exist in openlibrary.org")
#         print('### Book dont exist ###')
#         return HttpResponseRedirect(reverse('library:book-isbn'))
#
#     valido = {'title': 'The Little Prince', 'description': '', 'publish_date': None, 'authors': '<QuerySet[] >',
#               'image': '< SimpleUploadedFile: The Little Prince0156012197.jpg(image / jpeg) >', 'buy_date': None,
#               'holder': ''}
#     print(raw_data)
#     ## SERIALIZE DATA
#     book_dict = raw_data.get(f'ISBN:{isbn}', {})
#     image_url = book_dict.get('cover', {}).get('large')
#
#     title = book_dict.get('title')
#     # author = book_dict.get('authors')[0]['name']  # just grabing the first one to test
#     publish_date = book_dict.get('publish_date')
#     # add all data to be saved in db. image is appended in a different dict file_data
#     data = dict(isbn_10=isbn, title=title)
#     print('######################################')
#     print('Publish Date, Title, ImageURL, Book')
#     print(publish_date, title, image_url, book_dict)
#     print('######################################')
#     print('RAW DATA')
#     pprint(raw_data)
#     print('######################################')
#     print('######################################')
#
#     ### FILE HANDLING
#     import os
#     from urllib.parse import urlparse
#     # work the image around
#     form = None
#     if image_url:
#         parser = urlparse(image_url).path
#         image_name = os.path.basename(parser)  # this changes for the name of the book and so on
#         image_ext = os.path.splitext(image_name)[1]
#
#         # download and save image file in filesystem
#         image_bin = requests.get(image_url)
#         image_filename = os.path.join(settings.MEDIA_ROOT, 'books_cover', title + isbn + image_ext)
#         with open(image_filename, 'wb') as image:
#             image.write(image_bin.content)
#         # read file from filesystem
#         image = open(image_filename, 'rb')
#         # organized vaiadted data
#         file_data = {'image': SimpleUploadedFile(image_filename, image.read())}
#         form = BookForm(data=data, files=file_data)
#     ## VALIDATE DATA
#     # i need to add the author first if not yet in db. :s
#     if not form:
#         form = BookForm(data=data)
#
#     if form.is_valid():
#         messages.add_message(self.request, messages.SUCCESS, f"ISBN:{isbn} - And books' title is '{title}'")
#         print(form.cleaned_data)
#         book_obj = form.save()
#         return HttpResponseRedirect(reverse('library:book-update', args=[int(book_obj.id)]))
#
#     # add here the errors and soon as messages
#     # print(form.is_valid())
#     print(form.data)
#     # print(form.validate_unique())
#     # print(form.errors)
#     # print(form.changed_data)
#     # print(form.clean())
#     # print(form.cleaned_data.get('title'))
#     print(form.cleaned_data)
#
#     messages.add_message(self.request, messages.ERROR, f"ISBN:{isbn} - {str(form.cleaned_data)}")
#     return HttpResponseRedirect(reverse('library:book-isbn'))
#     # ConnectionError when no internet is available at own PC
#
#
# '''
# # input
# list = ['library.org',]
# # output
#
# isbn_10 = models.CharField(max_length=30, blank=True)
# title = models.CharField(max_length=300)
# subtitle = models.CharField(max_length=300)
#
# summary = models.TextField(blank=True)
# publish_date = models.DateField(blank=True, null=True)
# pages_num = models.IntegerField(blank=True, null=True)
#
# image = models.ImageField(
#     blank=True, null=True,
#     upload_to='books_cover/',
#     db_index=True,
# )
#
# # relationships
# authors = models.ManyToManyField('Author', related_name='books', blank=True)
# publishers = models.ManyToManyField('Publisher', related_name='books', blank=True)
# genres = models.ManyToManyField('Genre', related_name='books', blank=True)
# languages = models.ManyToManyField('Language', related_name='books', blank=True)
#
# # extra data
# buy_date = models.DateField(blank=True, null=True)
#
# # time
# created_at = models.DateTimeField('CreatedAt', auto_now_add=True)
# updated_at = models.DateTimeField('UpdatedAt', auto_now=True)
# '''

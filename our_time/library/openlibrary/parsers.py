class OpenLibraryParser:
    url = 'http://openlibrary.org/books/OL24229110M/IT'

    title = 'IT'
    by_statement = 'Stephen King.'
    publish_date = '1987-09'

    number_of_pages = 1093
    pagination = 'x, 1093 p. ;'

    publishers = [{'name': 'New American Library'}]
    authors = [{'name': 'Stephen King',
                'url': 'http://openlibrary.org/authors/OL2162284A/Stephen_King'}]

    cover = {'large': 'https://covers.openlibrary.org/b/id/8569281-L.jpg',
             'medium': 'https://covers.openlibrary.org/b/id/8569281-M.jpg',
             'small': 'https://covers.openlibrary.org/b/id/8569281-S.jpg'}

    notes = 'A Signet Book\r\nUS 4.95/CAN 5.95'
    publish_places = [{'name': 'New York, N.Y., USA'}]
    subject_people = [{'name': 'IT',
                       'url': 'https://openlibrary.org/subjects/person:it'}]
    subject_places = [{'name': 'Derry',
                       'url': 'https://openlibrary.org/subjects/place:derry'}]
    subject_times = [
        {'name': '1957',
         'url': 'https://openlibrary.org/subjects/time:1957'},
        {'name': '1958',
         'url': 'https://openlibrary.org/subjects/time:1958'}
    ]
    subjects = [
        {'name': 'coming of age',
         'url': 'https://openlibrary.org/subjects/coming_of_age'},
        {'name': 'thrillers',
         'url': 'https://openlibrary.org/subjects/thrillers'},
        {'name': 'suspense',
         'url': 'https://openlibrary.org/subjects/suspense'},
        {'name': 'horror',
         'url': 'https://openlibrary.org/subjects/horror'},
        {'name': 'Schwinn bicycles',
         'url': 'https://openlibrary.org/subjects/schwinn_bicycles'},
        {'name': 'catatonia',
         'url': 'https://openlibrary.org/subjects/catatonia'},
        {'name': 'homosexuality',
         'url': 'https://openlibrary.org/subjects/homosexuality'}
    ]

    def __init__(self, json_data):
        self.isbn, self.book_data = (
            self.extract_isbn_and_book(json_data)
        )

    def extract_isbn_and_book(self, json_data):
        isbn, book = next(iter(json_data.items()))
        isbn = isbn.replace('ISBN:', '').strip()
        return isbn, book

    def to_dict(self):
        return dict(
            isbn_10=self.isbn,
            title=self.parse_title(),
            subtitle=self.parse_subtitle(),
            description=self.parse_description(),
            publish_date=self.parse_publish_date(),
            number_of_pages=self.parse_number_of_pages(),
            # table_of_contents=self.parse_table_of_contents(),
            authors=self.parse_authors(),
            publishers=self.parse_publishers(),
            # genres=self.parse_genres(),
            # languages=self.parse_languages(),
            cover=self.parse_cover(),
        )

    def parse_title(self):
        return self.book_data.get('title', '')

    def parse_subtitle(self):
        return self.book_data.get('subtitle', '')

    def parse_description(self):
        return self.book_data.get('notes', '')

    def parse_publish_date(self):
        from dateutil import parser
        publish_date = self.book_data.get('publish_date', '').strip()

        # grab the first year "1961-71"
        if len(publish_date) == 6 and '-' in publish_date:
            publish_date = publish_date.split('-')[0]

        return parser.parse(publish_date).date()

    def parse_number_of_pages(self):
        return self.book_data.get('number_of_pages', '')

    def parse_table_of_contents(self):
        toc = self.book_data.get('table_of_contents', '')
        contents = [subject['title'] for subject in toc]
        return contents

    def parse_authors(self):
        authors = self.book_data.get('authors', [])
        return [author['name'] for author in authors]

    def parse_publishers(self):
        publishers = self.book_data.get('publishers', [])
        return [publisher['name'] for publisher in publishers]

    def parse_genres(self):
        genres = self.book_data.get('genres', [])
        return [genre['name'] for genre in genres]

    def parse_languages(self):
        return []

    def parse_cover(self):
        sizes = ['large', 'medium', 'small']
        images = self.book_data.get('cover', {})

        for size in sizes:
            if size in images:
                return images[size]
        else:
            return ''

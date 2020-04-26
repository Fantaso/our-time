class OpenLibraryParser:
    ###  jscmd = data
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
    # download available files in ebooks
    ebooks = [
        {'availability': 'full',  # 'restricted', 'borrow',
         'formats': {'epub': {'url': 'https://archive.org/download/CleanCode_201607/CleanCode_201607.epub'},
                     'pdf': {'url': 'https://archive.org/download/CleanCode_201607/CleanCode_201607.pdf'},
                     'text': {'url': 'https://archive.org/download/CleanCode_201607/CleanCode_201607_djvu.txt'}},
         'preview_url': 'https://archive.org/details/CleanCode_201607',
         'read_url': 'https://archive.org/stream/CleanCode_201607'}
    ]
    links = [
        {'title': 'Becoming by Michelle Obama | Crown '
                  'Publishing',
         'url': 'https://becomingmichelleobama.com/'},
        {'title': 'Becoming (book) - Wikipedia',
         'url': 'https://en.wikipedia.org/wiki/Becoming_(book)'},
        {'title': 'Reading Michelle Obama’s “Becoming” '
                  'as a Motherhood Memoir',
         'url': 'https://www.newyorker.com/culture/cultural-comment/reading-michelle-obamas-becoming-as-a-motherhood-memoir'},
        {'title': 'Becoming by Michelle Obama review – '
                  'race, marriage and the ugly side of '
                  'politics',
         'url': 'https://www.theguardian.com/books/2018/nov/14/michelle-obama-becoming-review-undoubtedly-political-book'},
        {'title': "Michelle Obama's memoir Becoming "
                  'sells 10 million copies - BBC News',
         'url': 'https://www.bbc.com/news/business-47704987'}
    ]
    classifications = {
        'dewey_decimal_class': ['909.82'],
        'lc_classifications': ['CB428 .H36848 '
                               '2018']
    }
    identifiers = {
        'goodreads': ['238540'],
        'isbn_10': ['0340750154'],
        'isbn_13': ['9780340750155'],
        'lccn': ['2018013856'],
        'oclc': ['1029771757'],
        'librarything': ['38872'],
        'openlibrary': ['OL9784448M']
    }

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
    weight = '1 grams'

    ###  jscmd = details
    description = '\"A study of voluntary slow reading from diverse angles\"--Provided by publisher.'
    physical_format = "Paperback"
    physical_dimensions = "1 x 1 x 1 inches"
    type = {"key": "/type/edition"}
    languages = [{"key": "/languages/eng"}]

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
            characters=self.parse_characters(),
            authors=self.parse_authors(),
            publishers=self.parse_publishers(),
            genres=self.parse_genres(),
            # languages=self.parse_languages(),
            cover=self.parse_cover(),
        )

    def parse_title(self):
        title = self.book_data.get('title', '')
        return self.clean_str(title)

    def parse_subtitle(self):
        subtitle = self.book_data.get('subtitle', '')
        return self.clean_str(subtitle)

    def parse_description(self):
        description = self.book_data.get('notes', '')
        return self.clean_str(description)

    def parse_publish_date(self):
        from dateutil import parser
        publish_date = self.book_data.get('publish_date', '').strip()

        # grab the first year "1961-71"
        if len(publish_date) == 7 and '-' in publish_date:
            publish_date = publish_date.split('-')[0]
        if publish_date:
            return parser.parse(publish_date).date()
        return ''

    def parse_number_of_pages(self):
        return self.book_data.get('number_of_pages', '')

    def parse_table_of_contents(self):
        toc = self.book_data.get('table_of_contents', '')
        contents = [self.clean_str(subject['title']) for subject in toc]
        return contents

    def parse_characters(self):
        characters = self.book_data.get('subject_people', [])
        return [self.clean_str(character['name']) for character in characters]

    def parse_authors(self):
        authors = self.book_data.get('authors', [])
        return [self.clean_str(author['name']) for author in authors]

    def parse_publishers(self):
        publishers = self.book_data.get('publishers', [])
        return [self.clean_str(publisher['name']) for publisher in publishers]

    def parse_genres(self):
        genres = self.book_data.get('subjects', [])
        return [self.clean_str(genre['name']) for genre in genres]

    def parse_languages(self):
        return []

    def clean_str(self, _str: str):
        return _str.strip().lower()

    def parse_cover(self):
        sizes = ['large', 'medium', 'small']
        images = self.book_data.get('cover', {})

        for size in sizes:
            if size in images:
                return images[size]
        else:
            return ''

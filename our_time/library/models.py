from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import cached_property


class NameRepr:
    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)
    nationality = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True)

    @cached_property
    def birthdate_year(self):
        if self.birthdate:
            return self.birthdate.strftime('%Y')
        return None

    @cached_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('-name',)
        verbose_name = 'author'
        verbose_name_plural = 'authors'


class Publisher(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.name}'


class Language(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    # book details
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    isbn_10 = models.CharField(max_length=30, blank=True)

    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    publish_date = models.DateField(blank=True, null=True)
    number_of_pages = models.IntegerField(blank=True, null=True)

    # relationships
    authors = models.ManyToManyField('Author', related_name='books', blank=True)
    publishers = models.ManyToManyField('Publisher', related_name='books', blank=True)
    genres = models.ManyToManyField('Genre', related_name='books', blank=True)
    languages = models.ManyToManyField('Language', related_name='books', blank=True)

    # media
    cover = models.ImageField(
        blank=True, null=True,
        upload_to='books_cover/',
        db_index=True,
    )

    @cached_property
    def year(self):
        if self.publish_date:
            return self.publish_date.strftime('%Y')
        return ''

    def __str__(self):
        return f'<book: {self.title} - {self.year}>'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('library:book-detail', args=[int(self.id)])

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'book'
        verbose_name_plural = 'books'

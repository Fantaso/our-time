from django.db import models
from django.utils.functional import cached_property


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)
    nationality = models.CharField(max_length=50)
    birthdate = models.DateField(blank=True, null=False)

    @cached_property
    def birthdate_year(self):
        return self.birthdate.strftime('%Y')

    @cached_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'<author: {self.full_name}:{self.birthdate_year}>'

    class Meta:
        ordering = ('-first_name',)
        verbose_name = 'author'
        verbose_name_plural = 'authors'


class Publisher(models.Model):
    name = models.CharField(max_length=120, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=15, blank=True)


class Language(models.Model):
    name = models.CharField(max_length=100, blank=True)


class Book(models.Model):
    isbn_10 = models.CharField(max_length=30, blank=True)
    isbn_13 = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    publish_date = models.DateField(blank=True, null=True)
    authors = models.ManyToManyField('Author', related_name='books', blank=True)
    image = models.ImageField(
        blank=True, null=True,
        upload_to='books_cover/',
        db_index=True,
    )
    pages_num = models.IntegerField(blank=True, null=True)
    publishers = models.ManyToManyField('Publisher', related_name='books', blank=True)
    genres = models.ManyToManyField('Genre', related_name='books', blank=True)
    languages = models.ManyToManyField('Language', related_name='books', blank=True)

    buy_date = models.DateField(blank=True, null=True)
    holder = models.CharField(max_length=100, blank=True)

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

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


class Book(models.Model):
    title = models.CharField(max_length=300)
    # image = models.ImageField()
    description = models.TextField()
    publish_date = models.DateField(blank=True, null=False)
    authors = models.ManyToManyField('Author', related_name='books')

    buy_date = models.DateField(blank=True, null=False)
    holder = models.CharField(max_length=100, blank=False, null=False)

    @cached_property
    def year(self):
        return self.publish_date.strftime('%Y')

    def __str__(self):
        return f'<book: {self.title} - {self.year}>'

    class Meta:
        ordering = ('-title',)
        verbose_name = 'book'
        verbose_name_plural = 'books'

# Generated by Django 2.2 on 2019-12-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20191219_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn_10',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]

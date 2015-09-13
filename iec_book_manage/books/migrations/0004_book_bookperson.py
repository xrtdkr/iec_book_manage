# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_book_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookPerson',
            field=models.ForeignKey(to='books.Person', null=True),
        ),
    ]

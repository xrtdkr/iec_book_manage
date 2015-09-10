# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bookName', models.CharField(max_length=20)),
                ('bookNum', models.CharField(max_length=20)),
                ('bookTime', models.DateTimeField(default=None)),
                ('bookFlag', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('personName', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='person',
            field=models.ForeignKey(related_name='person', blank=True, to='books.Person', null=True),
        ),
    ]

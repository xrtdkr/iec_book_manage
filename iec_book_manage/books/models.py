# coding:utf-8

import datetime
from django.db import models


class Person(models.Model):
    personName = models.CharField(max_length=20)

    def __unicode__(self):
        return self.personName


class Book(models.Model):
    bookName = models.CharField(max_length=20)
    bookNum = models.CharField(max_length=20)
    bookTime = models.DateTimeField(default=None)
    bookFlag = models.BooleanField(default=True)    # 布尔值True表示可借,布尔值为False不可借python
    bookPerson = models.ForeignKey(Person, null=True)

    def __unicode__(self):
        return self.bookName


# Create your models here.

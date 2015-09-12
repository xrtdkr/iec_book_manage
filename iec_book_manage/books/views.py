#-*-coding:utf-8-*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from books.models import *
from django.http import HttpResponse
from django.template import RequestContext
import datetime


def welcome(request):
    books = Book.objects.all()
    return render_to_response('welcome.html', {'book_set': books})


def secret(request):
    if 'book_name' and 'book_num' in request.POST:
        if request.POST['book_num'] and request.POST['book_name']:  #1,这里缺少了对于数据库的重复数据的查询.2,这里缺少对数据按照分类进行排序的判断
            book_num = request.POST['book_num']
            book_name = request.POST['book_name']
            now = datetime.datetime.now()
            book = Book(bookName=book_name)
            book.bookNum = book_num
            book.bookFlag = False
            book.bookTime = now
            book.save()
            book_set = Book.objects.all()
            return render_to_response('seccret.html', {'book_set': book_set}, context_instance=RequestContext(request))
        else:
            return HttpResponse('Sorry, you submit no book HaHa')  #这里设计的缺少合理之处:改进:1.变成重新渲染模板一下的网页提示2.使用ajax进行交互

    else:
        book_set = Book.objects.all()
        return render_to_response('seccret.html', {'book_set': book_set}, context_instance=RequestContext(request))











# Create your views here.

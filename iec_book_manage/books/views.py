#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response
from books.models import *
from django.http import HttpResponse
from django.template import RequestContext
import datetime

'''对于views的几点改进:1.名字不允许设置成为小写的xxx_set:全部改成统一的xxx_list.(已经改正)
   2.在看完foreignkey以后可以使用一下新的东西.并且关注一下那个foreignkey的报错(no default xxx in)
   3.以后的代码规范:采用在python中得变量全部用小写下划线,函数名和类名用驼峰式写法,其中函数名首字母小写而类名手字母大写'''


def welcome(request):
    books = Book.objects.all()
    return render_to_response('welcome.html', {'book_set': books})


def secret(request):
    if 'book_name' and 'book_num' in request.POST:
        if request.POST['book_num'] and request.POST['book_name']:  # 1,这里缺少了对于数据库的重复数据的查询.2,这里缺少对数据按照分类进行排序的判断
            book_num = request.POST['book_num']
            book_name = request.POST['book_name']
            book_list_lite = Book.objects.all()     # book_list_lite:这个query_Set为在book_list正式参与渲染模板之前所有的所有book对象的表
            for book_lite in book_list_lite:        # book_list:为参与渲染之前,现有的表中的对象
                book_lite

            '''now = datetime.datetime.now()
            book = Book(bookName=book_name)
            book.bookNum = book_num
            book.bookFlag = True
            book.bookTime = now'''

            book.save()
            book_list = Book.objects.all()
            return render_to_response('seccret.html', {'book_set': book_list}, context_instance=RequestContext(request))
        else:
            return HttpResponse('Sorry, you submit no book HaHa')  # 这里设计的缺少合理之处:改进:1.变成重新渲染模板一下的网页提示2.使用ajax进行交互

    else:
        book_list = Book.objects.all()
        return render_to_response('seccret.html', {'book_set': book_list}, context_instance=RequestContext(request))


def borrow(request):
    if 'bookNum' and 'Name' not in request.POST:  # 区分在request头文件里面的有key(键)和value(键值)为空的情况
        book_list = Book.objects.all()
        return render_to_response('borrow.html', {'book_set': book_list}, context_instance=RequestContext(request))
    elif request.POST['bookNum'] and request.POST['Name']:
        bookNum = request.POST['bookNum']
        name = request.POST['Name']  # name是借书人的名字
        # 上面两个把请求的头文件里面的信息的值变成python变量
        now = datetime.datetime.now()
        book = Book.objects.get(bookNum=bookNum)
        book.bookPerson = name
        book.bookTime = now
        book.Flag = False
        book.save()
        book_list = Book.objects.all()
        return render_to_response('borrow.html', {'book_set': book_list}, context_instance=RequestContext(request))
    else:
        return HttpResponse('sorry,the Ajax or remind is on building^~^,please been keeping curios')













# Create your views here.

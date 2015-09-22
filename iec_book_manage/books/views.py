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
            copy_flag = False
            for book_lite in book_list_lite:        # book_list:为参与渲染之前,现有的表中的对象
                if book_num == book_lite.bookNum and book_name == book_lite.bookName:  # 查重算法重新写
                    copy_flag = True
                    break                           # break注意一下用法
                else:
                    pass
            if not copy_flag:
                now = datetime.datetime.now()
                book = Book(bookName=book_name)
                book.bookNum = book_num
                book.bookFlag = True
                book.bookTime = now
                book.save()
            else:
                return HttpResponse('You commit a copy ^~^')  # 不可以简单粗暴地直接返回httpresponse改进:1变成重新渲染模板一下的网页提示2使用ajax进行交互
            book_list = Book.objects.all()
            return render_to_response('seccret.html',
                                      {'book_set': book_list},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse('Sorry, you submit no book HaHa')  # 这里设计的缺少合理之处:改进:1.变成重新渲染模板一下的网页提示2.使用ajax进行交互
    elif 'book_delete' in request.POST:
        if request.POST['book_delete']:    # 对请求的书本删除进行回应
            book_delete = request.POST['book_delete']
            book_list_lite = Book.objects.all()    # 同样的这个是临时的那个book表单
            # 对于无此匹配表单的回应:
            delete_flag = False
            for book_lite in book_list_lite:
                if book_delete == book_lite.bookNum:
                    delete_flag = True
                    break
            if not delete_flag:   # 这个地方其实需要改进的...因为对于大多数情况而言还是不要把对数据库的操作那么容易达成
                return HttpResponse('sorry,no book in database can match the book that you what to delete')
            else:
                Book.objects.filter(bookNum=book_delete).delete()
                book_list = Book.objects.all()
                return render_to_response('seccret.html',
                                          {'book_set': book_list},
                                          context_instance=RequestContext(request))    # 有匹配表单
        else:    # 对于空表单的回应
            return HttpResponse('你上传的是空表单,刷新一下页面回去重新填写哦')
    else:  # 这个else是用来回应直接请求网页的时候,给出渲染
        book_list = Book.objects.all()
        return render_to_response('seccret.html',
                                  {'book_set': book_list},
                                  context_instance=RequestContext(request))
    # secret 部分初步完成
    # secret 进一步完成,导致出错的原因:break没有用好.


# 注意在错误修改的时候,一定所有的东西都要去进行迭代,不可以迭代不利,半新半旧.
def borrow(request):
    if 'bookNum' and 'Name' not in request.POST:  # 区分在request头文件里面的有key(键)和value(键值)为空的情况
        book_list = Book.objects.all()
        return render_to_response('borrow.html',
                                  {'book_list': book_list},
                                  context_instance=RequestContext(request))
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
        return render_to_response('borrow.html',
                                  {'book_list': book_list},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponse('sorry,the Ajax or remind is on building^~^,please been keeping curios')
# borrow已经初步构建完成啦啦啦啦啦了


def returning(request):
    if 'person' in request.POST:
        if request.POST['person']:
            person_auth = request.POST['person']
            try:
                Person.objects.get(personName=person_auth)  # 这个只起到一个错误判断的作用,若执行通过则表示查有此人
                html = render_to_response('return_auth.html',
                                          context_instance=RequestContext(request))
                html.set_cookie('person_auth', person_auth)
                return html
            except:
                return HttpResponse('sorry!!! your name does not match')
        else:
            return HttpResponse('you submit an empty form')
    else:
        return render_to_response('return.html',
                                  context_instance=RequestContext(request))


'''checkbox的表单,和那个正常的表单是一样的,都是一个key对应一个value,然后name是名字,对应的name的键值,如果选中了的话,为"on",
没有选中的话则没有key键,而不是key值为空,'''


# 有一个错误:就是可以
def return_auth(request):   # auth在这里表示验证,验证return那个表单所填写的人物名字
    person_auth = request.COOKIES['person_auth']
    book_auth_set = Book.objects.filter(bookPerson=person_auth)
    flag = 0
    for book_auth in book_auth_set:
        if request.POST[book_auth]:
            flag = 1
            book_auth.bookPerson = ''
            book_auth.bookFlag = True
            book_auth.save()
    if not flag:
        return HttpResponse('sorry,no book detect by %s ' % book_auth)
    book_remain_list = Book.objects.all()
    return render_to_response('return_authed.html',
                              {'authed_book_list': book_remain_list},
                              context_instance=RequestContext(request))

# Create your views here.'''

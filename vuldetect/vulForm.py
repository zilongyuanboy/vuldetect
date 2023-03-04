# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   vulForm.py
@Author     :   zilongyuan
@datetime   :    2023/2/11
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf

# => GET 表单
def search_form(request):  # 提供表单页面, 或者提供表单和处理表单数据都写在一个函数里
    # 写在一个函数要注意几点：
    # 1. 模版html表单中的action参数要跳转指向自己的url；
    # 2. 模版html表单中要在末尾预留处理后的数据输出；
    # 3. 视图函数最后的return要将HttpResponse改为render, 注意参数字典
    ctx = {}
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        ctx['message'] = request.GET['q']
    else:
        ctx['message'] = ''
    return render(request, 'search_form.html', ctx)

def search(request):  # 处理表单页面
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = 'content is ' + request.GET['q']
    else:
        message = 'Null form'
    return HttpResponse(message)

# login  这里用GET做登陆页面的话，用户名和密码都会以明文的形式显示在url中,改为post则不会
def login_form(request):  # 提供登陆页面
    return render(request, 'login_form.html')

def login(request):  # 处理登陆操作
    request.encoding = 'utf-8'
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
    else:
        name = ''
    if 'pwd' in request.GET and request.GET['pwd']:
        pwd = request.GET['pwd']
    else:
        pwd = ''
    print('This login =====> ')
    return HttpResponse('<p> user name is :'+ name + '<br>'
                        + 'user pwd is :' + pwd + '</p>')

# => POST 表单
def search_post(request):
    ctx = {}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)

# upload data
'''
def upload(request):
    ctx = {}
    if request.POST:
        # ctx['code'] = request.POST['code']  # 接收表单数据 这只能到得文件的文件名
        # 分别接收文件的几种信息
        ctx['filename'] = request.FILES['code']['filename']
        ctx['context_type'] = request.FILES['code']['context-type']
        ctx['code'] = request.FILES['code']['content']
        ctx['rlt'] = request.POST['code']  # 用来存放处理结果
    return render(request, "upload.html", ctx)
'''

from .detectModel import handle_uploaded_file
from .form import UploadFileForm
from vulDL.modelDL import vulPredict

def upload(request):  # url: ip:8000/upload/
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)  # 绑定POST和FILES
        if form.is_valid():
            # res = handle_uploaded_file(request.FILES['file'])
            res = 'succeed'
            raw_file = form.cleaned_data.get("file")
            title = form.cleaned_data.get("title")
            res = vulPredict(raw_file)
            return HttpResponse('<p>file is ' + res + '</p>')
    else:
        form = UploadFileForm()
    return render(request, 'upload2.html', {'form': form})  # 和html有关系, 用之前的html就form.is_valid()是false, 修改后就可以, 原来是form表格的enctype参数双引号打成中文输入法了





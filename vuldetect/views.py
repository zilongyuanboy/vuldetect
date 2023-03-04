# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   views.py
@Author     :   zilongyuan
@datetime   :    2023/1/31
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

from django.http import HttpResponse
from django.shortcuts import render

def vullogin(request):
    # 设置一个默认打开的网页，以判断是否是用户，否则提示注册新用户
    return HttpResponse('<p>登陆成功</p>')

def vuldetect(request):
    # 接收用户提供的源代码，并返回可疑漏洞代码行
    context = {}
    return render(request, 'vuldetect.html', context)


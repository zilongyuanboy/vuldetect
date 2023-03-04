# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   vuldb.py
@Author     :   zilongyuan
@datetime   :    2023/2/11
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

from django.http import HttpResponse
from vulModel.models import vulUser  # 导入vulUser表 vulModel是文件夹即app名，models是文件即表的集合

# 验证用户
def valuser(request):
    # testname = 'user1'
    user = vulUser.objects.filter(id=1)
    if user:
        ans = 'have user: '  # user是querySet类型不能直接加
    else:
        ans = 'have not user!'
    print(user)
    return HttpResponse('<p>'+ans+'</p>')

# 注册用户
def logon(request):
    # 添加一条用户数据
    user = vulUser(name='user1', password='123456', datetime='2023-2-11')
    user.save()
    return HttpResponse('<p> add user1 </p>')

# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   detectModel.py
@Author     :   zilongyuan
@datetime   :    2023/2/13
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

def handle_uploaded_file(f):
    with open('./file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return 'handle_uploaded_file'
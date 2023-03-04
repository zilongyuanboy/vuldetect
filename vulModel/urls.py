# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   urls.py
@Author     :   zilongyuan
@datetime   :    2023/2/13
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

from django.urls import re_path, path
from . import views

urlpatterns = [
    # Upload File Without Using Model Form
    re_path(r'^upload1/$', views.file_upload, name='file_upload'),

    # Upload Files Using Model Form
    re_path(r'^upload2/$', views.model_form_upload, name='model_form_upload'),

    # Upload FIles Using AjaxUpload
    re_path(r'^upload3/$', views.ajax_form_upload, name='ajax_form_upload'),

    # View File List
    path('file/', views.file_list, name='file_list'),

    # manual upload
    re_path(r'^manual-upload/$', views.manual_upload, name='manual_upload'),
]

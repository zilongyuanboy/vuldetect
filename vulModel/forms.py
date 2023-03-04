# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   forms.py
@Author     :   zilongyuan
@datetime   :    2023/2/13
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

# clean方法对文件进行验证，以jpg、pdf、xlsx、txt结尾
# 关于表单自定义和验证见Django基础：表单forms的设计于使用
from django import forms
from .models import File  # 导入自定义模型File(自定义的文件表)

# => 1. Regular form
class FileUploadForm(forms.Form):  # 继承Form
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    upload_method = forms.CharField(label="Upload Method", max_length=50,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        # 做文件类型过滤
        file = self.cleaned_data['file']  # 取得文件
        ext = file.name.split('.')[-1].lower()  # 取文件后缀变小写
        if ext not in ["jpg", "pdf", "xlsx", "txt"]:
            raise forms.ValidationError("Only jpg, pdf, xlsx, txt files are allowed.")
        # return cleaned data is very important.
        return file

# => 2. Model form
# 记得在自定义模型File中通过upload_to参数指定文件存储位置，并对文件重命名
# 通过自定义模型File重建FileUploadModelForm
class FileUploadModelForm(forms.ModelForm):  # 继承ModelForm
    class Meta:
        model = File
        fields = ('file', 'upload_method',)
        widgets = {
            'upload_method': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    # 过滤文件类型
    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["jpg", "pdf", "xlsx", "txt"]:
            raise forms.ValidationError("Only jpg, pdf, xlsx, txt files are allowed.")
        # return cleaned data is very important.
        return file

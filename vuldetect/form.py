# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   form.py
@Author     :   zilongyuan
@datetime   :    2023/2/13
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""

from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    # title = forms.CharField(max_length=50)
    title = forms.CharField(label="Upload Method", max_length=50,
                            widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean_file(self):
        # filter file type
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ['txt']:
            raise forms.ValidationError("only txt files are allowed.")
        return file


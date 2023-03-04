# !usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@file       :   manual_form.py
@Author     :   zilongyuan
@datetime   :    2023/2/16
@License    :   (C)Copyright 2021-2023, zilongyuan
@brief      :      
"""
from django import forms
# form .models import File

# manual upload files
class ManualUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    upload_method = forms.CharField(label="Upload Method", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1]
        if ext not in ["txt"]:
            raise forms.ValidationError("Only txt files are allowed.")
        return file

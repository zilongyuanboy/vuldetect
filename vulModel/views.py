from django.shortcuts import render


# 一般文件上传的视图函数，提供form.cleaned_data.get('file')获取验证通过的文件,并调用自定义的处理函数
# 如果不是POST则在upload_form.html中渲染一个空的FileUploadForm, file_list 方法来显示文件清单
from django.shortcuts import render, redirect, HttpResponse
from .models import File  # 导入File模型（文件表）
from .forms import FileUploadForm, FileUploadModelForm

import os
import uuid
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat


# Create your views here.

# => 0. Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")  # 取得所要有文件，按照id排序
    return render(request, 'file_list.html', {'files': files})

# => 1. Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            # 如果用ModelForm则下面的这些处理可以由form.save()代替，如何直接return
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")  # 取出上传的文件
            new_file = File()  # 建立一个文件表(模型)
            new_file.file = handle_uploaded_file(raw_file)  # 返回media路径下的files/文件名
            new_file.upload_method = upload_method
            new_file.save()  # 建立一个新表后，要在控制台创建表结构(第一个命令好像只在第一次创建时用，后面就只用第二、三个命令就可以了)，$ python manage.py migrate $ python manage.py makemigrations vulModel  $ python manage.py migrate vulModel
            return redirect("/file/file")
    else:
        form = FileUploadForm()
    return render(request, 'upload_form.html', {'form': form, 'heading': 'Upload files with Regular Form'})

def handle_uploaded_file(file):
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # fiel path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)  # <=== 这里绝对路径可能有点问题
    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path


# => 2. upload file with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # 只需要保持就可以了，modelForm会自动将文件保存并重命名到自定义的File表指定的路径(路径由File表字段的upload_to参数指定)`
            return redirect("/file/file")
    else:
        form = FileUploadModelForm()

    return render(request, 'upload_form.html', {'form': form, 'heading': 'Upload files with ModelForm'})

# => 3. upload file with Ajax
def ajax_form_upload(request):
    return HttpResponse("<p>Ajax form upload pending!</p>")

# => 4. manual upload
from .manual_form import ManualUploadForm
def manual_upload(request):
    if request.method == "POST":
        form = ManualUploadForm(request.POST, request.FILES)  # 又可以了？先用了下面这个函数，再用现在这个函数又可以了？应该最优可能的是定义继承的form类中没重写cleaned_data的原因，因为form.is_valid()会调用cleaned_data()方法
        # form = FileUploadForm(request.POST, request.FILES)  # form的问题，好像只能用这个类？
        if form.is_valid():
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file = handle_uploaded_file(raw_file)  # 设置处理文件存储路径 在上文定义
            new_file.upload_method = upload_method
            new_file.save()
            return redirect("/file/file/")
    else:
        form = ManualUploadForm()
        # form = FileUploadForm()
    return render(request, 'manual_upload.html', {'form': form, 'heading': 'Upload files with manual upload files.'})




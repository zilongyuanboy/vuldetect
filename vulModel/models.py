from django.db import models
import os
import uuid


# => Create your models here.
class vulUser(models.Model):  # 表名
    name = models.CharField(max_length=20)  # 字段名
    password = models.CharField(max_length=20)  # 密码
    datetime = models.DateField()  # 注册日期

# => Define user directory path => manual 1
def user_directory_path(instance, filename):  # filename: meida/files/xxx.ext
    # 为用户的文件重命名并设置存放路径
    ext = filename.split('.')[-1]  # 文件后缀
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)  # 拼接用户文件名和后缀
    return os.path.join("files", filename)  # files/xxx.ext

class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)  # upload_to 参数指定文件存储地址
    upload_method = models.CharField(max_length=50, verbose_name="Upload Method")





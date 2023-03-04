"""vuldetect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views  # 导入页面视图函数 views是文件，视图函数的集合
from . import vuldb  # 导入模型视图函数 vuldb是文件，视图函数的集合
from . import vulForm  # 导入Form视图函数 vulForm是文件，视图函数集合

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vullogin/', views.vullogin),
    path('vuldetect/', views.vuldetect),
    path('valUser/', vuldb.valuser),
    path('logon/', vuldb.logon),
    # => GET
    path('search-form/', vulForm.search_form),
    path('search/', vulForm.search),
    path('login-form/', vulForm.login_form),
    path('login/', vulForm.login),
    # => POST
    path('search-post/', vulForm.search_post),
    path('upload/', vulForm.upload),
    # => three method upload
    path('file/', include("vulModel.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 绑定静态文件URL和文件路径

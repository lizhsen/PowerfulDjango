# -*- coding: utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url, include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, \
    LogOutView, IndexView
from MxOnline import settings

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogOutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_acitve'),
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^org/', include('organization.urls', namespace='org')),
    # 配置上传文件的处理函数
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 配置上传文件的处理函数
    url(r'^static/(?P<path>.*)/$', serve, {"document_root": settings.STATIC_ROOT}),
    # 课程相关url
    url(r'^course/', include('courses.urls', namespace='course')),
    # 用户相关
    url(r'^users/', include('users.urls', namespace='users')),
]
# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

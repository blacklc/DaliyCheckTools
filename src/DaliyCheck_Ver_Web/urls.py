#!/usr/bin/env python
#coding:utf-8

"""DaliyCheck_Ver_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from DaliyCheck_Ver_Web.views import login_view,logout_view,register

urlpatterns = [
    url(r'^$',login_view,{"register_info":None}),
    url(r"^(?P<register_info>[A-Za-z]+\s[A-Za-z]+\s[A-Za-z]+)",login_view), #用户注册成功后，跳转回登陆页面(匹配注册方法跳转的url)
    url(r'^logout/',logout_view),
    url(r'^register/',register),
    url(r'^daliycheck/',include('DaliyCheck.urls')), #定义自定义应用
    url(r'^admin/', admin.site.urls),
]

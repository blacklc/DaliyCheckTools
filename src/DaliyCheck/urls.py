#!/usr/bin/env python
#coding:utf-8

"""djproject URL Configuration

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

from django.conf.urls import *
from DaliyCheck.views import *
from DaliyCheck.models import NBU,IBMGuardium,F5_PoolInfo

"""
定义特定应用的url配置
"""
#URL继续顺序是自顶向下(同防火墙的ACL)
urlpatterns = [
    url(r"^$",index,{
         "template":"daliycheck_index.html",        #关键字参数字段对应view方法的各个参数
         "context":{}}),
    url(r"^start_query$",check_process),
    url(r"^machine_view$",query_machine),
    url(r"^machine_view/(?P<operation>\w+)$",machine_operation),
    url(r"^report_view$",create_report),
    url(r"^create_report$",create_report),
    url(r"^spider_nbu$",get_data_by_spider,{
         "model":NBU,
         "template_name":"nbu_view.html",
         "system_name":"nbu",
         "default_url":"https://182.12.113.12/appliance/SubmitLogin.action",
         "default_uname":"admin",
         "default_pwd":"123456",
         "urllist_name":"nbu:urls",}),
    url(r"^spider_ibm$",get_data_by_spider,{
         "model":IBMGuardium,
         "template_name":"ibm_view.html",
         "system_name":"ibm",
         "default_url":"https://102.2.82.123:8443",
         "default_uname":"admin",
         "default_pwd":"123456",
         "urllist_name":"ibmguardium:urls",}),
    url(r"^spider_f5$",get_data_by_spider,{
         "model":F5_PoolInfo,
         "template_name":"f5_view.html",
         "system_name":"f5",
         "default_url":"https://11.29.21.221:443",
         "default_uname":"admin",
         "default_pwd":"123456#",
         "urllist_name":"f5pool:urls",}),
    url(r"^spider_ag$",get_lockevent),
    url(r"^return$",clean_session),
]













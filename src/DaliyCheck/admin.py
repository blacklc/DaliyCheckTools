#!/usr/bin/env python
#coding:utf-8

from django.contrib import admin
from DaliyCheck.models import check_Report

# Register your models here.
class Daliycheck_Admin(admin.ModelAdmin):
    """
    Daliycheck管理类
    """
    list_display=("_ip","_hostname","_timestamp","_avalaiblespace","_strogeused",)
    search_fields=("_ip","_hostname","_timestamp")
    
#将类添加到管理工具    
admin.site.register(check_Report,Daliycheck_Admin)
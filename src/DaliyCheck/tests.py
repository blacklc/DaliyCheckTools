#!/usr/bin/env python
#coding:utf-8

from django.core.wsgi import get_wsgi_application

import time
import os
import sys

sys.path.append("/Users/lichen/Documents/workspace/DaliyCheck_Ver_Web/src/") #在PYTHONPATH内添加指定路径，保证之后import操作能够找到指定模块
os.environ['DJANGO_SETTINGS_MODULE'] = 'DaliyCheck_Ver_Web.settings' #指定当前django项目中的settings.py文件
application = get_wsgi_application() #获取在settings中已注册的应用

from DaliyCheck.models import check_Report,date_timestamp
# Create your tests here.

def format_timestamp(timestamp):
    """
    时间戳转换为日期
    """
    ISOTIMEFORMAT="%Y-%m-%d %H:%M:%S"
    ltime=time.localtime(timestamp)
    f_tstp=time.strftime(ISOTIMEFORMAT,ltime)
    return f_tstp

def test_model():
    """
    测试moudel
    """
    r_timestamp=time.time()
    r_date=format_timestamp(r_timestamp)
    d=date_timestamp.objects.create(_timestamp=r_timestamp,_date=r_date)
    r=check_Report.objects.create(
                                  _ip="172.16.5.130",
                                  _hostname="test1",
                                  _timestamp=d,
                                  _avalaiblespace=7,
                                  _strogeused=51,
                                  )

def main():
    test_model()
    
if __name__=="__main__":
    main()
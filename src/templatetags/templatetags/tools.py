#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年8月31日

@author: lichen
'''

import time
from django import template

register=template.Library()

def format_timestamp(value):
    """
    时间戳转换为日期
    
    :param  value
            时间戳
    :type   value float
    
    :return f_tstp 格式化后的时间戳字符串
    """
    
    ISOTIMEFORMAT="%Y-%m-%d %H:%M:%S"
    ltime=time.localtime(value)
    f_tstp=time.strftime(ISOTIMEFORMAT,ltime)
    return f_tstp

def clear_symbol(value,arg):
    """
    清除字符串内指定符号
    
    :param  value
            需要清理的字符串
    :type   value string
    
    :param  arg
            需清理的符号
    :type   arg string
    
    :return 清理后的字符串
    """
    
    return value.replace(arg,"")

def translating_dbserverStatus(value):
    """
    将参数_dbServertype翻译为自然语言
    
    :param  value
            参数_dbServertype
    :type   value string
    
    :return 翻译后的_dbServertype
    """
    if value=="Pass":
        value="运转正常"
    elif value=="Fail":
        value="引擎故障"
    else:
        value="未知状况"
    return value

def translating_stapqStatus(value):
    """
    将参数_stap_status翻译为自然语言
    
    :param  value
            参数_stap_status
    :type   value string
    
    :return 翻译后的_stap_status
    """
    
    if value=="Active":
        value="监控中"
    elif value=="Inactive":
        value="脱离监控"
    else:
        value="未知状况"
    return value

def translating_poolMemberStatus(value):
    """
    将参数_poolMember_status翻译为自然语言
    
    :param  value
            参数_poolMember_status
    :type   value string
    
    :return 翻译后的_poolMember_status
    """
    
    if value=="Active":
        value="主节点"
    elif value=="Standby":
        value="备节点"
    else:
        value="未知类型"
    return value

def translating_poolMemberImg(value):    
    """
    将参数_poolMember_Img翻译为自然语言
    
    :param  value
            参数_poolMember_Img
    :type   value string
    
    :return 翻译后的_poolMember_Img
    """
    if value=="green":
        value="正在运行"
    elif value=="black":
        value="未运行"
    else:
        value="未知状态"
    return value
    
    
    
#注册自定义过滤器
register.filter('format_timestamp', format_timestamp)
register.filter('clear_symbol', clear_symbol)
register.filter('translating_dbserverStatus', translating_dbserverStatus)
register.filter('translating_stapqStatus', translating_stapqStatus)
register.filter('translating_poolMemberStatus', translating_poolMemberStatus)
register.filter('translating_poolMemberImg', translating_poolMemberImg)

























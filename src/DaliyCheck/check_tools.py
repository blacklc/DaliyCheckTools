#!/usr/bin/env python
#coding:utf-8

'''
Created on 2016年10月17日

@author: lichen
'''

import base_class.OS_operation_base as os_operationbase
import ConfigParser
import Queue
import threading
import time
import xlsxwriter as xw
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from DaliyCheck.models import check_Report
from django.http import HttpResponse
from time import mktime, strptime

def format_date(date):
    """
    日期转换为时间戳
    
    :param  date
            格式化日期字符串
    :type   string
    
    :return timestamp 时间戳
    """
    ISOTIMEFORMAT="%Y-%m-%d %H:%M:%S"
    timestamp=mktime(strptime(date,ISOTIMEFORMAT))
    #timestamp=mktime(strptime(date.encode("utf-8"),ISOTIMEFORMAT))
    return timestamp

def format_timestamp(timestamp):
    """
    时间戳转换为日期
    
    :param  timestamp
            时间戳
    :type   string
    
    :return f_tstp 格式化后的日期
    """
    ISOTIMEFORMAT="%Y-%m-%d %H:%M:%S"
    ltime=time.localtime(timestamp)
    f_tstp=time.strftime(ISOTIMEFORMAT,ltime)
    return f_tstp

def readConfig(configfile):
    """
    读取配置文件:读取服务器IP地址保存在指定队列中;读取数据库配置信息;读取多进程配置信息
    
    :param  configfile
            配置文件全路径
    :type   string
    
    :return process_info 进程配置map 
            snmp_info snmp配置map
            system_info 业务系统名配置map 
            report_info 巡检报告配置map 
    """
    system_info=[]
    process_info={}
    snmp_info={}
    report_info={}
    config=ConfigParser.ConfigParser()
    config.read(configfile)
    process_config=config.items("PROCESS")
    snmp_config=config.items("SNMP")
    system_config=config.items("SYSTEM")
    report_config=config.items("REPORT")
    for pinfos in process_config:
        process_info[pinfos[0]]=pinfos[1]
    for snmpinfo in snmp_config:
        snmp_info[snmpinfo[0]]=snmpinfo[1]
    for systeminfo in system_config:
        system_info.append(systeminfo[1])
    for reportinfo in report_config:
        report_info[reportinfo[0]]=reportinfo[1]
    return process_info,snmp_info,system_info,report_info

def save_SU_In_DB(snmp_resultQueue,*args):
    """
    保存空间使用率至数据库中
    
    :param  snmp_resultQueue
            snmp查询结果队列
    :type   multiprocessing.Manager.Queue
    
    :param  *args
            可选参数：args[0][0]：hostname_map,args[0][1]:date_timestap
    :type   tupel
    
    :return Null
    """
    try:
        result_map=snmp_resultQueue.get(block=False)
        snmp_resultQueue.task_done() 
        for key in result_map:
            r=check_Report.objects.create(
                _ip=key,
                _hostname=args[0][0][key],
                _timestamp=args[0][1],
                _strogeused=int(result_map[key][0]),
            )      
    except Queue.Empty:
        print "snmp_resultQueue(SU) is empty"
        
def save_AG_In_DB(snmp_resultQueue):
    """
    保存可用空间至数据库中
    :param  snmp_resultQueue
            snmp查询结果队列
    :type   multiprocessing.Manager.Queue
    
    :return Null
    """  
    try:
        result_map=snmp_resultQueue.get(block=False)
        snmp_resultQueue.task_done() 
        for key in result_map:
            update_num=check_Report.objects.filter(_ip=key).update(_avalaiblespace=int(result_map[key][0])/(1024*1024))
    except Queue.Empty:
        print "snmp_resultQueue(AG) is empty"
    
def save_multiprocess(thead_methd,snmp_resultQueue,*args):
    """
    数据库存储多进程方法
    
    :param  thead_methd
            线程操作方法名
    :type   fuction
    
    :param  snmp_resultQueue
            snmp查询结果队列
    :type   multiprocessing.Manager.Queue
    
    :param  *args
            可选参数：args[0][0]：hostname_map,args[0][1]:date_timestap
    :type   tupel
    
    :return Null
    """
    while not snmp_resultQueue.empty():
        #调用多线程完成ping指令
        if args:
            thread_worker1=threading.Thread(target=thead_methd,args=(snmp_resultQueue,(args[0][0],args[0][1])))
            thread_worker2=threading.Thread(target=thead_methd,args=(snmp_resultQueue,(args[0][0],args[0][1])))
            thread_worker3=threading.Thread(target=thead_methd,args=(snmp_resultQueue,(args[0][0],args[0][1])))
            thread_worker4=threading.Thread(target=thead_methd,args=(snmp_resultQueue,(args[0][0],args[0][1])))
            thread_worker5=threading.Thread(target=thead_methd,args=(snmp_resultQueue,(args[0][0],args[0][1])))
        else:
            thread_worker1=threading.Thread(target=thead_methd,args=(snmp_resultQueue,))
            thread_worker2=threading.Thread(target=thead_methd,args=(snmp_resultQueue,))
            thread_worker3=threading.Thread(target=thead_methd,args=(snmp_resultQueue,))
            thread_worker4=threading.Thread(target=thead_methd,args=(snmp_resultQueue,))
            thread_worker5=threading.Thread(target=thead_methd,args=(snmp_resultQueue,))
        thread_worker1.start()
        thread_worker2.start()
        thread_worker3.start()
        thread_worker4.start()
        thread_worker5.start()
        thread_worker1.join()
        thread_worker2.join()
        thread_worker3.join()
        thread_worker4.join()
        thread_worker5.join()

def save_machine_StorageUsed(_snmp,alive_machineList,_manager,hostname_map,date_timestap):
    """
    存储空间使用率
    
    :param  _snmp
            snmp_base实例
    :type   base_class.Snmp_base.snmp_base
    
    :param  alive_machineList
            存活主机列表
    :type   list
    
    :param  _manager
            multiprocessing.Manager实例
    :type   multiprocessing.Manager
    
    :param  hostname_map
            主机名与ip对应map
    :type   dict
    
    :param  date_timestap
            时间戳
    :type   string
    
    :return error_list 错误列表
    """
    error_list=[]
    o=os_operationbase.os_operation_base() # base_class.OS_operation_base.os_operationbases实例
    alive_machineQueue=_manager.Queue(maxsize=100)
    snmp_resultQueue=_manager.Queue(maxsize=100)
    error_machineQueue=_manager.Queue(maxsize=100)
    _snmp.oid=".1.3.6.1.4.1.2021.9.1.9.1"
    _snmp.get_machineInfo(alive_machineList,alive_machineQueue,snmp_resultQueue,error_machineQueue) # 调用snmpget指令
    o.run_multiprocess(4,save_multiprocess,(save_SU_In_DB,snmp_resultQueue,(hostname_map,date_timestap))) # 保存至数据库
    while not error_machineQueue.empty():
        error_list.append(error_machineQueue.get())
        error_machineQueue.task_done()
    return error_list
            
def save_machine_AvalaibleSpace(_snmp,alive_machineList,_manager):
    """
    存储可用空间
    
    :param  _snmp
            snmp_base实例
    :type   base_class.Snmp_base.snmp_base
    
    :param  alive_machineList
            存活主机列表
    :type   list
    
    :param  _manager
            multiprocessing.Manager实例
    :type   multiprocessing.Manager
    
    :return error_list 错误列表
    """
    error_list=[]
    o=os_operationbase.os_operation_base() # base_class.OS_operation_base.os_operationbases实例
    alive_machineQueue1=_manager.Queue(maxsize=100)
    snmp_resultQueue1=_manager.Queue(maxsize=100)
    error_machineQueue1=_manager.Queue(maxsize=100)
    _snmp.oid=".1.3.6.1.4.1.2021.9.1.7.1"
    _snmp.get_machineInfo(alive_machineList,alive_machineQueue1,snmp_resultQueue1,error_machineQueue1) # 调用snmpget指令
    o.run_multiprocess(4,save_multiprocess,(save_AG_In_DB,snmp_resultQueue1)) # 保存至数据库
    while not error_machineQueue1.empty():
        error_list.append(error_machineQueue1.get())
        error_machineQueue1.task_done()
    return error_list

def create_excel(system_list,date):
    """
    生成巡检报告
    
    :param  system_list
            业务系统名列表
    :type   list
    
    :param  date
            巡检日期
    :type   string
    
    :return response 返回response对象(下载表格)
    """
    #报告背景颜色
    bgc=["CCFFCC","CCFFFF","FFFF99","99CCFF","FF99CC","CC99FF","FFCC99","33CCCC","666699"]
    bgc_id=0
    #建立游标
    cursor=1
    #create a workbook in memory
    output = StringIO.StringIO()
    #创建xlsx文件
    workbook=xw.Workbook(output)
    #在文件中新建一个sheet
    worksheet=workbook.add_worksheet("daliycheck_report")
    #设置格式
    title_format=workbook.add_format()
    title_format.set_align("vcenter") 
    title_format.set_align("center")
    title_format.set_bg_color("FFCC99")
    title_format.set_border()
    detail_fromat=workbook.add_format()
    detail_fromat.set_align("vcenter") 
    detail_fromat.set_align("center")
    detail_fromat.set_border()
    #设置行格式
    worksheet.set_column("A:F",15)
    #写入指定单元格(若增加新列务必要修改后边的列数迭代处)
    worksheet.write(0,0,"System",title_format)
    worksheet.write(0,1,"IP",title_format)
    worksheet.write(0,2,"HostName",title_format)
    worksheet.write(0,3,"Date",title_format)
    worksheet.write(0,4,"AvalaibleSpace(G)",title_format)
    worksheet.write(0,5,"StorgeUesd(%)",title_format)
    for name in system_list:
        query_report=check_Report.objects.filter(
                                                 _timestamp___date__contains=date,
                                                 _hostname__contains=name,
                                                 ).order_by("id")
        #计算报告内容条数
        result_number=query_report.count()
        #合并单元格
        system_name_format=workbook.add_format()
        system_name_format.set_align("vcenter") 
        system_name_format.set_align("center")
        system_name_format.set_bg_color(bgc[bgc_id])
        system_name_format.set_border()
        if result_number>1:
            worksheet.merge_range(cursor, 0, cursor+result_number-1, 0, name,system_name_format)
        else:
            worksheet.write(cursor,0,name,system_name_format)
        #将结果写入表中
        save_object={}
        #行数迭代
        for i,r in zip(range(cursor,cursor+result_number),query_report):
            #匹配业务系统主机
            #临时存储查询结果对象
            save_object[1]=r.ip
            save_object[2]=r.hostname
            save_object[3]=r.timestamp.date
            save_object[4]=r.avalaiblespace
            save_object[5]=r.strogeused
            #列数迭代
            for y in range(1,6):
                worksheet.write(i,y,save_object[y],detail_fromat)
        cursor=cursor+result_number
        if bgc_id==8:
            bgc_id=0
        else:
            bgc_id=bgc_id+1
    workbook.close()
    #创建保存xlsx文件类型的httpresponse对象
    output.seek(0)
    response=HttpResponse(output.read(),content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["content-Disposition"]="attachment;filename=DaliyCheck_Report-%s.xlsx"%(time.strftime("%Y-%m-%d"))
    return response

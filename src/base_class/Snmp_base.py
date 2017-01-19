#!/usr/bin/env python2.7
#coding:utf-8

'''
Created on 2016年6月30日

@author: lichen
'''

import copy_reg
import netsnmp
import Queue
import threading
import time
import types

from multiprocessing import Pool
from random import uniform

def _pickle_method(m):
    '''
    用copy_reg将当前类注册为可序列化，以便进程池调用
    '''
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class snmp_base(object):
    '''
    snmp相关操作基础类
    '''
    __slots__=("__oid","__version","__destHost","__community")

    def __init__(self):
        self.__oid=None
        self.__version=2
        self.__destHost=None
        self.__community="public"

    def get_community(self):
        return self.__community


    def set_community(self, value):
        self.__community = value


    def get_oid(self):
        return self.__oid


    def get_version(self):
        return self.__version


    def get_dest_host(self):
        return self.__destHost


    def set_oid(self, value):
        self.__oid = value


    def set_version(self, value):
        self.__version = value


    def set_dest_host(self, value):
        self.__destHost = value

    oid = property(get_oid, set_oid, None, None)
    version = property(get_version, set_version, None, None)
    destHost = property(get_dest_host, set_dest_host, None, None)
    community = property(get_community, set_community, None, None)
    
    
    def run_multiprocess(self,process_num,process_target,process_args):
        '''
        多进程执行方法
        
        :param  process_num
                进程池大小
        :type   int
        
        :param  process_target
                进程执行方法
        :type   Method
        
        :param  process_args
                进程执行方法的参数元组
        :type   tuple
        
        :return Null
        '''
        #创建指定数量的进程池
        process_pool=Pool(processes=process_num)
        #指定并行执行的进程数量
        for i in range(process_num):
            process_pool.apply_async(process_target,args=process_args)
        process_pool.close() # 关闭pool；即不能再添加进程
        process_pool.join() # 等待所有子进程执行完毕

    def querySysInfo_By_snmpwalk(self):
        '''
        查询系统信息(基于snmpwalk方式)
        
        :return qurey_result 查询结果
        :type string
        '''
        try:
            qurey_result=netsnmp.snmpwalk(self.__oid,Version=self.__version,DestHost=self.__destHost,Community=self.__community)
        except Exception,err:
            print "snmpget walk:",err
            qurey_result=None
        return qurey_result
    
    def querySysInfo_By_snmpwalk_ver_mp(self,desthost_queue,result_queue,error_queue):
        '''
        查询系统信息(基于snmpwalk方式,多进程,需要配合run_multiprocess使用)
        
        :param  desthost_queue
                需查询主机IP地址队列
        :type   multiprocessing.Manager.Queue
        
        :param  result_queue
                查询结果队列
        :type   multiprocessing.Manager.Queue
        
        :param  error_queue
                错误队列
        :type   multiprocessing.Manager.Queue
        
        :return Null
        '''
        time.sleep(uniform(0,2))
        while not desthost_queue.empty():
            result_map={}
            self.__destHost=desthost_queue.get()
            try:
                qurey_result=netsnmp.snmpwalk(self.__oid,Version=self.__version,DestHost=self.__destHost,Community=self.__community)
                if qurey_result[0]==None:
                    print self.__destHost,"snmpwalk None"
                    error_queue.put(self.__destHost)
                else:
                    result_map[self.__destHost]=qurey_result
                    result_queue.put(result_map)
            except Exception,err:
                print "snmpget walk:",err
                error_queue.put(self.__destHost)
        
    def querySysInfo_By_snmpget(self):
        '''
        查询系统信息(基于snmpget方式)
        
        :return qurey_result 查询结果
        :type string
        '''
        try:
            qurey_result=int(netsnmp.snmpget(self.__oid,Version=self.__version,DestHost=self.__destHost,Community=self.__community)[0])
        except Exception,err:
            print "snmpget error:",err
            qurey_result=None
        return qurey_result
    
    def sysInfo_By_Snmpget(self,desthost_queue,result_queue,error_queue):
        """
        使用snmpget获取系统相关信息
        
        :param  desthost_queue
                目标主机IP队列
        :type   multiprocessing.Manager.Queue
        
        :param  result_queue
                保存snmp结果队列
        :type   multiprocessing.Manager.Queue
        
        :param  error_queue
                snmpget操作失败主机队列
        :type   multiprocessing.Manager.Queue
        
        :return Null
        """
        result_map={}
        try:
            destHost=desthost_queue.get(block=False)
            desthost_queue.task_done()
            qurey_result=netsnmp.snmpget(self.__oid,Version=self.__version,DestHost=destHost,Community=self.__community)
            if qurey_result[0]==None:
                error_queue.put(destHost)
            else:
                result_map[destHost]=qurey_result
                result_queue.put(result_map)
        except Queue.Empty:
            print "desthost_queue is empty"  
        except Exception,err:
            print "snmpget error:",err
            error_queue.put(destHost)
        
    def querySysInfo_By_snmpget_ver_mp(self,desthost_queue,result_queue,error_queue):
        '''
        查询系统相关信息(基于snmpget方式,多进程,需要配合run_multiprocess使用)
        
        :param  desthost_queue
                需查询主机IP地址队列
        :type   multiprocessing.Manager.Queue
        
        :param  result_queue
                查询结果队列
        :type   multiprocessing.Manager.Queue
        
        :param  error_queue
                错误队列
        :type   multiprocessing.Manager.Queue
        
        :return Null
        ''' 
        while not desthost_queue.empty():
            #调用多线程完成snmpget指令
            thread_worker1=threading.Thread(target=self.sysInfo_By_Snmpget,args=(desthost_queue,result_queue,error_queue))
            thread_worker2=threading.Thread(target=self.sysInfo_By_Snmpget,args=(desthost_queue,result_queue,error_queue))
            thread_worker3=threading.Thread(target=self.sysInfo_By_Snmpget,args=(desthost_queue,result_queue,error_queue))
            thread_worker4=threading.Thread(target=self.sysInfo_By_Snmpget,args=(desthost_queue,result_queue,error_queue))
            thread_worker5=threading.Thread(target=self.sysInfo_By_Snmpget,args=(desthost_queue,result_queue,error_queue))
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
    
    def get_machineInfo(self,alive_machineList,alive_machineQueue,snmp_resultQueue,error_machineQueue):
        '''
        获取集群各主机信息(基于snmpget方式,多进程,需要配合run_multiprocess使用)
        
        :param  alive_machineList
                存活主机列表
        :type   list
        
        :param  manager
                multiprocessing.manager对象
        :type   multiprocessing.Manager
        
        :return Null
        '''
        for am in alive_machineList:
            alive_machineQueue.put(am)
        self.run_multiprocess(4,self.querySysInfo_By_snmpget_ver_mp,(alive_machineQueue,snmp_resultQueue,error_machineQueue))
        """
        while not snmp_resultQueue.empty():
            result_map=snmp_resultQueue.get()
            result_list.append(result_map)
        while not error_machine.empty():
            error_ma=error_machine.get()
            error_list.append(error_ma)
        return result_list,error_list
            #for key in result_map:
                #print "Host %s's Percentage of space used on disk:%d%%" %(key,int(result_map[key][0]))
        """
    


#!/usr/bin/env python
#coding:utf-8

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models

class machine_info(models.Model):
    """
    巡检机器信息
    """

    def get_ostype(self):
        return self._ostype


    def get_addtime(self):
        return self._addtime


    def set_ostype(self, value):
        self._ostype = value


    def set_addtime(self, value):
        self._addtime = value


    def del_ostype(self):
        del self._ostype


    def del_addtime(self):
        del self._addtime


    def get_ipaddress(self):
        return self._ipaddress


    def get_hostname(self):
        return self._hostname


    def set_ipaddress(self, value):
        self._ipaddress = value


    def set_hostname(self, value):
        self._hostname = value


    def del_ipaddress(self):
        del self._ipaddress


    def del_hostname(self):
        del self._hostname

    _ipaddress=models.CharField(max_length=45, blank=True)
    _hostname=models.CharField(max_length=100, blank=True, null=True)
    _ostype=models.CharField(max_length=60, blank=True, null=True)
    #_addtime=models.FloatField(blank=True, null=True)
    _addtime=models.CharField(max_length=100, blank=True, null=True)
        
    ipaddress = property(get_ipaddress, set_ipaddress, del_ipaddress, "ipaddress's docstring")
    hostname = property(get_hostname, set_hostname, del_hostname, "hostname's docstring")
    ostype = property(get_ostype, set_ostype, del_ostype, "ostype's docstring")
    addtime = property(get_addtime, set_addtime, del_addtime, "addtime's docstring")
    
class date_timestamp(models.Model):         
    """
    纪录时间戳于自然语言日期对应
    """

    def get_timestamp(self):
        return self._timestamp


    def get_date(self):
        return self._date


    def set_timestamp(self, value):
        self._timestamp = value


    def set_date(self, value):
        self._date = value


    def del_timestamp(self):
        del self._timestamp


    def del_date(self):
        del self._date

    _timestamp = models.FloatField(blank=True, null=True)
    _date=models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering=['-_timestamp']
    
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    date = property(get_date, set_date, del_date, "date's docstring")

class check_Report(models.Model):
    """
    巡检结果模型
    """
    
    def get_ip(self):
        return self._ip


    def get_hostname(self):
        return self._hostname


    def get_timestamp(self):
        return self._timestamp


    def get_avalaiblespace(self):
        return self._avalaiblespace


    def get_strogeused(self):
        return self._strogeused


    def set_ip(self, value):
        self._ip = value


    def set_hostname(self, value):
        self._hostname = value


    def set_timestamp(self, value):
        self._timestamp = value


    def set_avalaiblespace(self, value):
        self._avalaiblespace = value


    def set_strogeused(self, value):
        self._strogeused = value


    def del_ip(self):
        del self._ip


    def del_hostname(self):
        del self._hostname


    def del_timestamp(self):
        del self._timestamp


    def del_avalaiblespace(self):
        del self._avalaiblespace


    def del_strogeused(self):
        del self._strogeused


    _ip = models.CharField(max_length=45, blank=True, null=True)
    _hostname = models.CharField(max_length=100, blank=True, null=True)
    _timestamp = models.ForeignKey(date_timestamp)
    _avalaiblespace = models.IntegerField(blank=True, null=True)
    _strogeused = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering=['-_timestamp']
        
    ip = property(get_ip, set_ip, del_ip, "ip's docstring")
    hostname = property(get_hostname, set_hostname, del_hostname, "hostname's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    avalaiblespace = property(get_avalaiblespace, set_avalaiblespace, del_avalaiblespace, "avalaiblespace's docstring")
    strogeused = property(get_strogeused, set_strogeused, del_strogeused, "strogeused's docstring")
        

class lock_event(models.Model):
    """
    数据库阻塞事件模型
    """

    def get_event_pid(self):
        return self._eventPID


    def get_ip(self):
        return self._ip


    def get_hostname(self):
        return self._hostname


    def get_result_pid(self):
        return self._resultPID


    def get_timestamp(self):
        return self._timestamp


    def get_sql(self):
        return self._sql


    def set_event_pid(self, value):
        self._eventPID = value


    def set_ip(self, value):
        self._ip = value


    def set_hostname(self, value):
        self._hostname = value


    def set_result_pid(self, value):
        self._resultPID = value


    def set_timestamp(self, value):
        self._timestamp = value


    def set_sql(self, value):
        self._sql = value


    def del_event_pid(self):
        del self._eventPID


    def del_ip(self):
        del self._ip


    def del_hostname(self):
        del self._hostname


    def del_result_pid(self):
        del self._resultPID


    def del_timestamp(self):
        del self._timestamp


    def del_sql(self):
        del self._sql



    _eventPID= models.CharField(max_length=20, blank=True, null=True)
    _hostname=models.CharField(max_length=40, blank=True, null=True)
    _resultPID=models.CharField(max_length=20, blank=True, null=True)
    _timestamp=models.FloatField(blank=True, null=True)
    _sql=models.CharField(max_length=10000, blank=True, null=True)
    
    class Meta:
        ordering=['_timestamp']
        
    eventPID = property(get_event_pid, set_event_pid, del_event_pid, "eventPID's docstring")
    ip = property(get_ip, set_ip, del_ip, "ip's docstring")
    hostname = property(get_hostname, set_hostname, del_hostname, "hostname's docstring")
    resultPID = property(get_result_pid, set_result_pid, del_result_pid, "resultPID's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")
    sql = property(get_sql, set_sql, del_sql, "sql's docstring")
    

class F5_PoolInfo(models.Model):
    """
    F5 Pool信息模型
    """

    def get_pool_member_img(self):
        return self._poolMember_Img


    def get_pool_member_name(self):
        return self._poolMember_name


    def get_pool_member_status(self):
        return self._poolMember_status


    def get_pool_name(self):
        return self._poolName


    def get_timestamp(self):
        return self._timestamp


    def set_pool_member_img(self, value):
        self._poolMember_Img = value


    def set_pool_member_name(self, value):
        self._poolMember_name = value


    def set_pool_member_status(self, value):
        self._poolMember_status = value


    def set_pool_name(self, value):
        self._poolName = value


    def set_timestamp(self, value):
        self._timestamp = value


    def del_pool_member_img(self):
        del self._poolMember_Img


    def del_pool_member_name(self):
        del self._poolMember_name


    def del_pool_member_status(self):
        del self._poolMember_status


    def del_pool_name(self):
        del self._poolName


    def del_timestamp(self):
        del self._timestamp



    _poolMember_Img=models.CharField(max_length=10, blank=True, null=True)
    _poolMember_name=models.CharField(max_length=20, blank=True, null=True)
    _poolMember_status=models.CharField(max_length=10, blank=True, null=True)
    _poolName=models.CharField(max_length=50, blank=True, null=True)
    _timestamp=models.FloatField(blank=True, null=True)
    
    poolMember_Img = property(get_pool_member_img, set_pool_member_img, del_pool_member_img, "poolMember_Img's docstring")
    poolMember_name = property(get_pool_member_name, set_pool_member_name, del_pool_member_name, "poolMember_name's docstring")
    poolMember_status = property(get_pool_member_status, set_pool_member_status, del_pool_member_status, "poolMember_status's docstring")
    poolName = property(get_pool_name, set_pool_name, del_pool_name, "poolName's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")


class IBMGuardium(models.Model):
    """
    IBMGuardium模型
    """

    def get_db_server_status(self):
        return self._dbServer_Status


    def get_db_servertype(self):
        return self._dbServertype


    def get_ip(self):
        return self._ip


    def get_stap_status(self):
        return self._stap_status


    def get_timestamp(self):
        return self._timestamp


    def set_db_server_status(self, value):
        self._dbServer_Status = value


    def set_db_servertype(self, value):
        self._dbServertype = value


    def set_ip(self, value):
        self._ip = value


    def set_stap_status(self, value):
        self._stap_status = value


    def set_timestamp(self, value):
        self._timestamp = value


    def del_db_server_status(self):
        del self._dbServer_Status


    def del_db_servertype(self):
        del self._dbServertype


    def del_ip(self):
        del self._ip


    def del_stap_status(self):
        del self._stap_status


    def del_timestamp(self):
        del self._timestamp



    _dbServer_Status=models.CharField(max_length=20, blank=True, null=True)
    _dbServertype=models.CharField(max_length=20, blank=True, null=True)
    _ip=models.CharField(max_length=20, blank=True, null=True)
    _stap_status=models.CharField(max_length=50, blank=True, null=True)
    _timestamp=models.FloatField(blank=True, null=True)
    
    dbServer_Status = property(get_db_server_status, set_db_server_status, del_db_server_status, "dbServer_Status's docstring")
    dbServertype = property(get_db_servertype, set_db_servertype, del_db_servertype, "dbServertype's docstring")
    ip = property(get_ip, set_ip, del_ip, "ip's docstring")
    stap_status = property(get_stap_status, set_stap_status, del_stap_status, "stap_status's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")

class NBU(models.Model):
    """
    NBU模型
    """

    def get_avail_storage_space(self):
        return self._availStorageSpace


    def get_avail_storage_space_in_percent(self):
        return self._availStorageSpaceInPercent


    def get_used_storage_space(self):
        return self._usedStorageSpace


    def get_used_storage_space_in_percent(self):
        return self._usedStorageSpaceInPercent


    def get_timestamp(self):
        return self._timestamp


    def set_avail_storage_space(self, value):
        self._availStorageSpace = value


    def set_avail_storage_space_in_percent(self, value):
        self._availStorageSpaceInPercent = value


    def set_used_storage_space(self, value):
        self._usedStorageSpace = value


    def set_used_storage_space_in_percent(self, value):
        self._usedStorageSpaceInPercent = value


    def set_timestamp(self, value):
        self._timestamp = value


    def del_avail_storage_space(self):
        del self._availStorageSpace


    def del_avail_storage_space_in_percent(self):
        del self._availStorageSpaceInPercent


    def del_used_storage_space(self):
        del self._usedStorageSpace


    def del_used_storage_space_in_percent(self):
        del self._usedStorageSpaceInPercent


    def del_timestamp(self):
        del self._timestamp

    
    
    _availStorageSpace=models.CharField(max_length=20, blank=True, null=True)
    _availStorageSpaceInPercent=models.CharField(max_length=20, blank=True, null=True)
    _usedStorageSpace=models.CharField(max_length=20, blank=True, null=True)
    _usedStorageSpaceInPercent=models.CharField(max_length=20, blank=True, null=True)
    _timestamp=models.FloatField(blank=True, null=True)
    
    availStorageSpace = property(get_avail_storage_space, set_avail_storage_space, del_avail_storage_space, "availStorageSpace's docstring")
    availStorageSpaceInPercent = property(get_avail_storage_space_in_percent, set_avail_storage_space_in_percent, del_avail_storage_space_in_percent, "availStorageSpaceInPercent's docstring")
    usedStorageSpace = property(get_used_storage_space, set_used_storage_space, del_used_storage_space, "usedStorageSpace's docstring")
    usedStorageSpaceInPercent = property(get_used_storage_space_in_percent, set_used_storage_space_in_percent, del_used_storage_space_in_percent, "usedStorageSpaceInPercent's docstring")
    timestamp = property(get_timestamp, set_timestamp, del_timestamp, "timestamp's docstring")















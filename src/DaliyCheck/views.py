#!/usr/bin/env python
#coding:utf-8


import base_class.Snmp_base as snmp_base
import base_class.OS_operation_base as os_operationbase
import redis
import time

from check_tools import readConfig,save_machine_AvalaibleSpace,save_machine_StorageUsed,create_excel,format_date,format_timestamp
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import  HttpResponseRedirect
from DaliyCheck.models import check_Report,date_timestamp,machine_info,lock_event
from django.shortcuts import render
from multiprocessing import Manager

# Create your views here.

def query_machine(request):
    """
    主机操作:查询
    """
    query_error=[]
    if request.method=="POST" or request.session.get("machine_queryset_atime",None) or request.session.get("machine_queryset_ip",None):
        #必填项
        if request.method=="POST":
            if (not request.POST.get("atime",None)) and (not request.POST.get("ip",None)):  # get():如果取到返回values；若没有键则给该键赋值逗号后的值
                query_error.append("请输入需要查询的IP地址或添加时间")
        if not query_error or request.session.get("machine_queryset_atime",None) or request.session.get("machine_queryset_ip",None):
            try:
                #使用添加日期查找
                #if request.POST["atime"] and (not request.POST["ip"]):
                if (not request.POST.get("ip",None)) and (request.POST.get("atime",None) or request.session.get("machine_queryset_atime",None)) and (request.POST.get("atime",None) or (not request.session.get("machine_queryset_ip",None))):
                    if request.POST.get("atime",None):
                        queryset=request.POST["atime"]
                        request.session["machine_queryset_atime"]=request.POST["atime"] # 保存用户查询条件
                        request.session["machine_queryset_ip"]=None
                    else:
                        queryset=request.session["machine_queryset_atime"]
                        request.session["machine_queryset_ip"]=None
                    stag="atime"
                    query_report=machine_info.objects.filter(_addtime__contains=queryset).order_by("id")
                # 使用ip查询
                #elif (not request.POST["atime"]) and request.POST["ip"]:
                elif (not request.POST.get("atime",None)) and (request.POST.get("ip",None) or request.session.get("machine_queryset_ip",None)) and (request.POST.get("ip",None) or (not request.session.get("machine_queryset_atime",None))):
                    if request.POST.get("ip",None):
                        queryset=request.POST["ip"]
                        request.session["machine_queryset_ip"]=request.POST["ip"] # 保存用户查询条件
                        request.session["machine_queryset_atime"]=None
                    else:
                        queryset=request.session["machine_queryset_ip"]
                        request.session["machine_queryset_atime"]=None
                    stag="ip"
                    query_report=machine_info.objects.filter(_ipaddress__contains=queryset).order_by("id")
                # 使用日期和ip查询
                else:
                    #if not query_error:
                    if request.POST.get("ip",None):
                        queryset_atime=request.POST["atime"]
                        queryset_ip=request.POST["ip"]
                        request.session["machine_queryset_atime"]=request.POST["atime"]
                        request.session["machine_queryset_ip"]=request.POST["ip"]
                    else:
                        queryset_atime=request.session["machine_queryset_atime"]
                        queryset_ip=request.session["machine_queryset_ip"]
                    stag="ai"
                    query_report=machine_info.objects.filter(
                                    _addtime__contains=queryset_atime,
                                    _ipaddress__contains=queryset_ip,
                                ).order_by("id")
                paginator = Paginator(query_report,5) # 每页显示5个对象
                page = request.GET.get('page') # 获取当前显示页数
                contacts = paginator.page(page) # 查询应显示的多个对象
            except PageNotAnInteger:
                contacts = paginator.page(1) # 如果前台没有传递page,则默认显示第一页.
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages) # 如果前台传递的page大于总页数，则显示最后一页
            except:
                print "Query Error or Session Error"
                contacts=None
            finally:
                context={"query_report":contacts}
                if contacts != None:
                    context["suces_fail"]="query_success"
                if request.POST.get("ip",""):
                    context["ip"]=request.POST.get("ip","")
                else:
                    context["ip"]=request.session.get("machine_queryset_ip","")
                if request.POST.get("atime",""):
                    context["atime"]=request.POST.get("atime","")
                else:
                    context["atime"]=request.session.get("machine_queryset_atime","")
                context["stag"]=stag
                context["errors"]=query_error
                template="machine_view.html"
                return render(request,template,context)
    # 若发现输入错误，则返回原有页面
    context={
        "errors":query_error,
        "ip":"",
        "atime":"",
        "stag":"",
        "suces_fail":"query_fail",
    }
    template="machine_view.html"
    return render(request,template,context)

def machine_operation(request,operation):
    """
    添加，修改或删除巡检机器
    
    :param  operation
            用户操作类型
    :type   string
    """
    query_error=[]
    if request.method=="POST":
        if (not request.POST.get("q_ip","")):  # get():如果取到返回values；若没有键则给该键赋值逗号后的值
            query_error.append("请输入主机IP地址")
        if not query_error:
            q_ip=request.POST["q_ip"]
            # 添加主机
            if operation=="add":
                if request.POST["new_hostname"]:
                    hostname=request.POST["new_hostname"]
                else:
                    hostname=None
                if request.POST["new_ostype"]:
                    ostype=request.POST["new_ostype"]
                else:
                    ostype=None
                timestamp=time.time()
                addtime=format_timestamp(timestamp)
                m=machine_info.objects.create(_ipaddress=q_ip,_hostname=hostname,_ostype=ostype,_addtime=addtime)
                context={"query_report":m,"suces_fail":"add_suces",}
                template="machine_view.html"
                return render(request,template,context)                     
            # 修改主机
            elif operation=="update":
                old_m=machine_info.objects.get(_ipaddress=q_ip)
                if request.POST["update_ip"]:
                    ip=request.POST["update_ip"]
                else:
                    ip=q_ip
                if request.POST["update_hostname"]:
                    hostname=request.POST["update_hostname"]
                else:
                    hostname=old_m.hostname
                if request.POST["update_ostype"]:
                    ostype=request.POST["update_ostype"]
                else:
                    ostype=old_m.ostype
                addtime=old_m.addtime               
                update_num=machine_info.objects.filter(_ipaddress=q_ip).update(
                                                                            _ipaddress=ip,
                                                                            _hostname=hostname,
                                                                            _ostype=ostype,
                                                                            _addtime=addtime
                                                                        )
                if q_ip==ip:
                    query_report=machine_info.objects.filter(_ipaddress__contains=q_ip,).order_by("id")
                else:
                    query_report=machine_info.objects.filter(_ipaddress__contains=ip,).order_by("id")
                
                context={"query_report":query_report,"suces_fail":"update_suces",}
                template="machine_view.html"
                return render(request,template,context)  
            # 删除主机
            elif operation=="delete":
                machine_info.objects.filter(_ipaddress=q_ip).delete()
                context={"suces_fail":"delete_suces",}
                template="machine_view.html"
                return render(request,template,context)
    # 若发现输入错误，则返回原有页面
    context={
        "errors":query_error,
        "suces_fail":"fail",
    }
    template="machine_view.html"
    return render(request,template,context)
        

def check_process(request):
    """
    巡检操作
    """
    packet_loss={} # 存储主机丢包率map
    hostname_map={} # 主机名与ip对应map
    manager=Manager() # multiprocessing.Manager实例
    all_machineList=[] # 主机IP列表
    alive_machineList=[] # 存活主机IP列表
    r_timestamp=time.time() # 巡检时间戳
    s=snmp_base.snmp_base() # base_class.Snmp_base.snmp_base实例
    o=os_operationbase.os_operation_base() #base_class.OS_operation_base.os_operationbases实例
    all_machine=manager.Queue(maxsize=100) # 全部主机IP队列
    alive_machine=manager.Queue(maxsize=100) # 存活主机队列
    # 读取配置文件
    process_config,snmp_config,system_list,report_config=readConfig("/Users/lichen/Documents/workspace/DaliyCheck_Ver_Web/src/resources/config.ini")
    # 配置snmp
    s.version=int(snmp_config["version"])
    s.community=snmp_config["community"]
    minfo_report=machine_info.objects.all() # 获取机器IP
    for m in minfo_report:
        all_machine.put(m.ipaddress)
        hostname_map[m.ipaddress]=m.hostname # 建立主机名与ip关系组
        all_machineList.append(m.ipaddress) # 保存所有机器ip
    o.run_multiprocess(int(process_config["poolsize"]),o.query_alive,(all_machine,alive_machine)) # 心跳检测
    # 持久化queue
    while not alive_machine.empty():
        host_map=alive_machine.get()
        alive_machine.task_done()
        for ip in host_map:
            alive_machineList.append(ip)
            packet_loss[ip]=host_map[ip]
    r_date=format_timestamp(r_timestamp) # 将时间戳转换为自然语言日期
    d=date_timestamp.objects.create(_timestamp=r_timestamp,_date=r_date) # 存储巡检时间
    error_list_su=save_machine_StorageUsed(s,alive_machineList,manager,hostname_map,d) # 获取空间使用率
    error_list_as=save_machine_AvalaibleSpace(s,alive_machineList,manager) # 获取剩余空间
    # 计算巡检失败机器信息
    if list(set(error_list_su).difference(set(error_list_as))):
        error_list=error_list_su
    else:
        differ_member=list(set(error_list_su).difference(set(error_list_as)))
        error_list_su[len(error_list_su):len(error_list_su)]=differ_member
        error_list=error_list_su
    dead_machineList=list(set(all_machineList).difference(set(alive_machineList))) # 计算心跳失败机器信息
    # 返回巡检失败机器信息页面 
    if dead_machineList or error_list:
        context={}
        if dead_machineList:
            context["d_ip"]=dead_machineList
        if error_list:
            context["e_ip"]=error_list
        return render(request,"result_view.html",context)
    return HttpResponseRedirect("/daliycheck") # 若无错误，则返回首页

def create_report(request):
    """
    生成巡检报告(xlsx格式)
    """
    error=[]
    # 生成报告内容
    if request.method=="POST":
        # 必填项
        if (not request.POST.get("date","")):  # get():如果取到返回values；若没有键则给该键赋值逗号后的值
            error.append("请输入需要查询的业务系统名或巡检日期")
        if not error:
            # 使用日期查找
            if request.POST["date"] and (not request.POST["appname"]):
                # 读取配置文件
                process_config,snmp_config,system_list,report_config=readConfig("/Users/lichen/Documents/workspace/DaliyCheck_Ver_Web/src/resources/config.ini")
            # 使用日期和主机名查询
            else:
                system_list=[]
                system_list.append(request.POST["appname"])
            response=create_excel(system_list,request.POST["date"]) # 创建巡检报告
            return response
    # 若发现输入错误，则返回原有页面
    context={
        "errors":error,
        "suces_fail":"create_fail",
    }
    template="create_report.html"
    return render(request,template,context)

def get_data_by_spider(request,model,template_name,system_name,default_url,default_uname,default_pwd,urllist_name):
    """
    获取实时信息.发布爬取任务以及提供相关网页信息.
    
    :param  template_name
            调用模版名称
    :type   template_name string

    :param  system_name
            爬取的web服务名称
    :type   system_name string
    
    :param  default_url
            爬取默认url
    :type   default_url string
    
    :param  default_uname
            web服务默认登录名
    :type   default_uname string
    
    :param  default_pwd
            web服务默认密码
    :type   default_pwd string
    
    :param  urllist_name
            爬虫start_url队列名
    :type   urllist_name string
    
    :return  
    """
    
    redis_client=redis.StrictRedis(host="localhost",port=6379,db=0) # 建立redis对象
    if request.method=="POST":
        # 确定web页面url
        if not request.POST.get("%s_url" %(system_name),None):
            if not request.session.get("default_%surl" %(system_name),None):
                url=default_url # 默认url 
            else:
                url=request.session["default_%surl" %(system_name)]
        else:
            url=request.POST["%s_url" %(system_name)]
            request.session["default_%surl" %(system_name)]=request.POST["%s_url" %(system_name)]
        if not request.POST.get("%s_username" %(system_name),None):
            # 保存上一次输入的用户名
            if redis_client.hget("login", "%s_username" %(system_name)):
                username=redis_client.hget("login", "%s_username" %(system_name))
            else:
                username=default_uname # 默认用户名
                redis_client.hmset("login",{"%s_username" %(system_name):username}) # 保存默认登陆用户名
        else:
            username=request.POST["%s_username" %(system_name)]
            redis_client.hmset("login",{"%s_username" %(system_name):username}) # 保存登陆用户名
        if not request.POST.get("%s_password" %(system_name),None):
            # 保存上一次输入的密码
            if redis_client.hget("login", "%s_password" %(system_name)):
                password=redis_client.hget("login", "%s_password" %(system_name))
            else:
                password=default_pwd # 默认密码
                redis_client.hmset("login",{"%s_password" %(system_name):password}) # 保存默认登陆密码
        else:
            password=request.POST["%s_password" %(system_name)]
            redis_client.hmset("login",{"%s_password" %(system_name):password}) # 保存登陆密码
        redis_client.lpush(urllist_name, url) # 将nbu_url加入待爬取队列中
        #redis_client.hmset("login",{"%s_username" %(system_name):username,"%s_password" %(system_name):password}) #保存登陆用户名密码
        request.session["%s_start" %(system_name)]=True

    try:
        query_report=model.objects.order_by("-_timestamp") # 按时间戳从倒叙查询爬取结果
        # 分页
        paginator = Paginator(query_report,10) # 每页显示10个对象
        page = request.GET.get('page') # 获取当前显示页数
        contacts = paginator.page(page) # 查询应显示的多个对象
    except PageNotAnInteger:
        contacts = paginator.page(1) # 如果前台没有传递page,则默认显示第一页.
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages) # 如果前台传递的page大于总页数，则显示最后一页
    except:
        print "Query Error or Session Error"
        contacts=None
    finally:
        notification="False"
        if request.session.get("%s_start" %(system_name),None):
            if request.session["%s_start" %(system_name)]:
                notification="True"
                request.session["%s_start" %(system_name)]=False
        if not request.session.get("default_%surl" %(system_name),None):
            last_url=default_url
            last_username=default_uname
        else:
            last_url=request.session["default_%surl" %(system_name)]
            last_username=redis_client.hget("login", "%s_username" %(system_name))
        context={
            "query_report":contacts,
            "notification":notification,
            "url":last_url,
            "username":last_username,
        }
        template=template_name
        del redis_client #关闭redis连接
        return render(request,template,context)

def get_lockevent(request):
    """
    获取实时阻塞事件
    """  
    try:
        query_report=lock_event.objects.order_by("-_timestamp") # 按时间戳倒叙查询爬取结果
        #分页
        paginator = Paginator(query_report,10) # 每页显示10个对象
        page = request.GET.get('page') # 获取当前显示页数
        contacts = paginator.page(page) # 查询应显示的多个对象
    except PageNotAnInteger:
        contacts = paginator.page(1) # 如果前台没有传递page,则默认显示第一页.
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages) # 如果前台传递的page大于总页数，则显示最后一页
    except:
        print "Query Error or Session Error"
        contacts=None
    finally:
        context={"query_report":contacts,}
        template="lockevent_view.html"
        return render(request,template,context)            
            
def index(request,template,context):
    """
    查询历史巡检纪录
    """
    error=[]
    # 判断是否是首次登陆到此应用(页面)
    if request.method=="POST" or request.session.get("index_queryset_date",None) or request.session.get("index_queryset_ip",None):
        # 必填项
        if request.method=="POST":
            if (not request.POST.get("date",None)) and (not request.POST.get("ip",None)):  # get():如果取到返回values；若没有键则给该键赋值逗号后的值
                error.append("请输入需要查询的IP地址或巡检时间")
        if not error or request.session.get("index_queryset_date",None) or request.session.get("index_queryset_ip",None):
            try:
                # 使用日期查找
                if (not request.POST.get("ip",None)) and (request.POST.get("date",None) or request.session.get("index_queryset_date",None)) and (request.POST.get("date",None) or (not request.session.get("index_queryset_ip",None))):
                    if request.POST.get("date",""):
                        queryset=request.POST["date"]
                        request.session["index_queryset_date"]=request.POST["date"] # 保存用户查询条件
                        request.session["index_queryset_ip"]=None
                    else:
                        queryset=request.session["index_queryset_date"]
                        request.session["index_queryset_ip"]=None
                    stag="date"
                    query_report=check_Report.objects.filter(_timestamp___date__contains=queryset).order_by("id")
                # 使用ip查询
                elif (not request.POST.get("date",None)) and (request.POST.get("ip",None) or request.session.get("index_queryset_ip",None)) and (request.POST.get("ip",None) or (not request.session.get("index_queryset_date",None))):
                    if request.POST.get("ip",""):
                        queryset=request.POST["ip"] 
                        request.session["index_queryset_ip"]=request.POST["ip"] # 保存用户查询条件
                        request.session["index_queryset_date"]=None
                    else:
                        queryset=request.session["index_queryset_ip"]
                        request.session["index_queryset_date"]=None
                    stag="ip" 
                    query_report=check_Report.objects.filter(_ip__contains=queryset).order_by("id")
                # 使用日期和ip查询
                else:
                    if request.POST.get("date",None):
                        queryset_date=request.POST["date"]
                        queryset_ip=request.POST["ip"]
                        request.session["index_queryset_date"]=request.POST["date"] # 保存用户查询条件
                        request.session["index_queryset_ip"]=request.POST["ip"] # 保存用户查询条件
                    else:
                        queryset_date=request.session["index_queryset_date"]
                        queryset_ip=request.session["index_queryset_ip"]
                    stag="di"
                    query_report=check_Report.objects.filter(
                                    _timestamp___date__contains=queryset_date,
                                    _ip__contains=queryset_ip,
                                ).order_by("id")
                paginator = Paginator(query_report,10) # 每页显示10个对象
                page = request.GET.get('page') # 获取当前显示页数
                contacts = paginator.page(page) # 查询应显示的多个对象
            except PageNotAnInteger:
                contacts = paginator.page(1)  # 如果前台没有传递page,则默认显示第一页.
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)  # 如果前台传递的page大于总页数，则显示最后一页
            except:
                print "Query Error or Session Error"
                contacts=None
            finally:
                context["query_report"]=contacts
                if request.POST.get("ip",""):
                    context["ip"]=request.POST.get("ip","")
                else:
                    context["ip"]=request.session.get("index_queryset_ip","")
                if request.POST.get("date",""):
                    context["date"]=request.POST.get("date","")
                else:
                    context["date"]=request.session.get("index_queryset_date","")
                context["stag"]=stag
                context["errors"]=error
                return render(request,template,context)
    # 首次登陆应用主页或输入错误查询条件自动跳回主页
    try:
        last_report=check_Report.objects.order_by("_timestamp")[0]
        query_report=check_Report.objects.filter(_timestamp=last_report.timestamp).order_by("id")
        paginator = Paginator(query_report,10) # 每页显示10个对象
        page = request.GET.get('page') # 获取当前显示页数
        contacts = paginator.page(page) # 查询应显示的多个对象
    except PageNotAnInteger:
        contacts = paginator.page(1) # 如果前台没有传递page,则默认显示第一页.
    except EmptyPage:
        #如果前台传递的page大于总页数，则显示最后一页
        contacts = paginator.page(paginator.num_pages)
    except:
        print "Query error"
        contacts=None
    finally:
        context["query_report"]=contacts
        context["errors"]=error
        context["ip"]=""
        context["date"]=""
        context["stag"]=""
        return render(request,template,context)
        
def clean_session(request):
    """
    清除用户查询条件，返回首页
    """
    if request.session.get("index_queryset_date",""):
        request.session["index_queryset_date"]=""
    if request.session.get("index_queryset_ip",""):
        request.session["index_queryset_ip"]=""
    if request.session.get("machine_queryset_atime",""):
        request.session["machine_queryset_atime"]="" 
    if request.session.get("machine_queryset_ip",""):
        request.session["machine_queryset_ip"]=""   
    return HttpResponseRedirect("/daliycheck/")
    
    
    
    
    
    
    
    
    
    












    
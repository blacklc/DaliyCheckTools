#!/usr/bin/env python
#coding:utf-8

from django.contrib import auth
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

def login_view(request,register_info):
    """
    处理用户登陆.使用django的认证系统
    
    :param  register_info
            注册完成标示
    :type   string
    """
    error=[]
    # 判断用户是否已经登陆
    if request.user.is_authenticated():
        return HttpResponseRedirect("/daliycheck/") # 实现已登陆自动跳转页面
    # 若通过post提交表单(登陆操作)
    if request.method=="POST":
        # 必填项
        if (not request.POST.get("username","")):# get():如果取到返回values；若没有键则给该键赋值逗号后的值
            error.append("请输入登陆用户名")
        if not error:
            if request.POST["username"]:
                username=request.POST["username"]
            else:
                username=None
            if request.POST["password"]:
                password=request.POST["password"]
            else:
                password=None
            user=auth.authenticate(username=username,password=password) # 验证用户的证书(合法性)
            # 判断用户是否可以登陆以及合法
            if user is not None and user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect("/daliycheck/")
            # 判断用户是否被锁定
            elif user is not None:
                error.append("该用户已被锁定，请通知管理员解锁此账户")
            # 否则用户不存在
            else:
                error.append("请输入正确的密码或该用户名不存在")
    context={"errors":error,"register_info":register_info} # 若是第一次登陆(没有通过post提交任何表单)此页面或注销后，则返回初始表单
    return render(request,"login.html",context)# 在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可

def logout_view(request):
    """
    处理用户注销，使用django的认证系统
    """
    auth.logout(request)
    return HttpResponseRedirect("/")

def register(request):
    """
    处理用户注册，使用django的内置表单
    """
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            return HttpResponseRedirect("/Creating user scussefull/")
    else:
        form=UserCreationForm()
    context={"form":form}
    return render(request,"register.html", context)# 在1.10版本后使用Requestcontext就使用此方法(django.shortcuts render)即可


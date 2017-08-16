# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue

# Create your views here.
def index(request):
    # 如果已登录则跳转到实验台
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    # 如果未登录展现登录界面
    else:
        template = get_template('login.html')
        return HttpResponse(template.render(locals()))

def home(request):
    # 如果已登录展现控制台
    if request.user.is_authenticated():
        template = get_template('home.html')
        return HttpResponse(template.render(locals()))
    # 如果未登录则跳转到首页
    else:
        return HttpResponseRedirect('/')

def mywork(request):
    # 如果已登录展现我的作业
    if request.user.is_authenticated():
        user = request.user.username
        template = get_template('mywork.html')
        return HttpResponse(template.render(locals()))
    # 如果未登录则跳转到首页
    else:
        return HttpResponseRedirect('/')

def myinfo(request):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    user = request.user.username
    template = get_template('myinfo.html')
    q = User.objects.filter(studentid=user)[0]
    return HttpResponse(template.render(locals()))
    

        


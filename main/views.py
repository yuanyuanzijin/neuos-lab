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
    # 如果未登录跳回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    user = request.user.username
    issue = 1
    template = get_template('home.html')
    qu = User.objects.get(student_id=user)
    qi_all = Issue.objects.all()
    qh = Homework.objects.get(student_id=user, issue_id=issue)
    return HttpResponse(template.render(locals()))
        

def mywork(request):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    user = request.user.username
    issue = 1
    template = get_template('mywork.html')
    qu = User.objects.get(student_id=user)
    qi = Issue.objects.get(id=issue)
    qh = Homework.objects.get(student_id=user, issue_id=issue)
    return HttpResponse(template.render(locals()))

def myinfo(request):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    user = request.user.username
    template = get_template('myinfo.html')
    q = User.objects.filter(student_id=user)[0]
    return HttpResponse(template.render(locals()))
    

        


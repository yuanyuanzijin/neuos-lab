# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue

############################ 登录界面 ############################################################
def index(request):
    # 如果未登录展现登录界面
    if not request.user.is_authenticated():
        template = get_template('login.html')
        return HttpResponse(template.render(locals()))

    # 查看是否是本课堂老师或学生，是则做相应的跳转，不是则展现不是本课堂学生的界面
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 1:
            return HttpResponseRedirect('/home')
        else:
            return HttpResponseRedirect('/teacher')
    else:
        context = {}
        context['allow'] = False
        return render(request, 'login.html', context)

########################### 学生功能界面 ###########################################################
def home(request):
    # 如果未登录跳回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # 查看是否是本课堂老师或学生，是则做相应的跳转，不是则跳回首页
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 1:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/teacher')
    else:
        return HttpResponseRedirect('/')

    issue = 1
    template = get_template('home.html')
    qi_all = Issue.objects.all()
    qh = Homework.objects.filter(student_id=user, issue_id=issue)
    if qh:
        qh = qh[0]
    
    return HttpResponse(template.render(locals()))
        

def mywork(request):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    issue = 1
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 1:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/teacher')
    else:
        return HttpResponseRedirect('/')
    
    template = get_template('mywork.html')
    qi = Issue.objects.filter(id=issue)
    if qi:
        qi = qi[0]
    qh = Homework.objects.filter(student_id=user, issue_id=issue)
    if qh:
        qh = qh[0]
    return HttpResponse(template.render(locals()))

def myinfo(request):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 1:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/teacher')
    else:
        return HttpResponseRedirect('/')

    template = get_template('myinfo.html')
    return HttpResponse(template.render(locals()))
    
######################## 老师功能界面 ###################################################
def teacher(request):
    # 如果未登录跳回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # 查看是否是本课堂老师或学生，是则做相应的跳转，不是则跳回首页
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')

    permission = True
    template = get_template('teacher/teacher.html')
    qi_all = Issue.objects.all()
    qh_all_submit = Homework.objects.filter(issue_id=1, repo__isnull=False)
    qh_all_pass = Homework.objects.filter(issue_id=1, check_result=True)
    submit_num = len(qh_all_submit)
    pass_num = len(qh_all_pass)
    return HttpResponse(template.render(locals()))

def students(request):
    # 如果未登录跳回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # 查看是否是本课堂老师或学生，是则做相应的跳转，不是则跳回首页
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')

    permission = True
    template = get_template('teacher/students.html')
    qs_all = User.objects.filter(user_type=1).order_by('student_id')
    qs_all_num = len(qs_all)
    return HttpResponse(template.render(locals()))

def issues(request):
    # 如果未登录跳回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # 查看是否是本课堂老师或学生，是则做相应的跳转，不是则跳回首页
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/')

    issue = 1
    permission = True
    template = get_template('teacher/issues.html')
    qi = Issue.objects.filter(id=issue)[0]
    qh_all = Homework.objects.filter(issue_id=issue)
    return HttpResponse(template.render(locals()))
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from django.utils import timezone
from django.contrib import auth
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

    template = get_template('home/home.html')
    qi_all = Issue.objects.all()
    homework_list = []
    for qi in qi_all:
        qh = Homework.objects.filter(student_id__student_id=user, issue_id=qi.id)
        if qh:
            homework_list.append({
                'qi': qi,
                'qh': qh[0]
            })
        else :
            homework_list.append({
                'qi': qi,
                'qh': {}
            })
    return HttpResponse(template.render(locals()))
        

def mywork(request, id):
    # 如果未登录则跳转到首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    issue_num = range(1, Issue.objects.count() + 1)
    if id:
        issue = int(id)
    else:
        issue = Issue.objects.count()
        return HttpResponseRedirect('/home/mywork/'+str(issue))
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 1:
            qu = qu[0]
        else:
            return HttpResponseRedirect('/teacher')
    else:
        return HttpResponseRedirect('/')
    
    template = get_template('home/mywork.html')
    qi_all = Issue.objects.all()  # 所有布置的作业
    qi = Issue.objects.filter(id=issue)
    if qi:
        qi = qi[0]
    qh = Homework.objects.filter(student_id__student_id=user, issue_id=issue)
    if qh:
        qh = qh[0]
    if issue >= 2:
        tmp = 1
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

    qi_all = Issue.objects.all()  # 所有布置的作业
    template = get_template('home/myinfo.html')
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
    qi_all = Issue.objects.all()                                                # 所有布置的作业
    qh_list = []
    for qi in qi_all:
        qh_all = Homework.objects.filter(issue_id=qi.id)                                # 作业1所有下载(学生下载实验环境后才会在Homework表插入数据)
        download_num = len(qh_all)                                                    # 锁业1所有下载数

        qh_all_submit = qh_all.filter(repo__isnull=False)                                  # 作业1所有提交
        submit_num = len(qh_all_submit)                                             # 作业1所有提交数

        qh_all_pass = qh_all.filter(check_result=1)                                     # 作业1所有通过
        pass_num = len(qh_all_pass)                                                 # 作业1所有通过数
        qh_list.append({
            'qi': qi,
            'qh_all': qh_all,
            'download_num': download_num,
            'qh_all_submit': qh_all_submit,
            'submit_num': submit_num,
            'qh_all_pass': qh_all_pass,
            'pass_num': pass_num
        })

    qs_all = User.objects.filter(user_type=1)                                   # 所有学生
    student_num = len(qs_all)                                                   # 所有学生数

    qs_all_github = qs_all.filter(github__isnull=False)
    github_num = len(qs_all_github)

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
    qi_all = Issue.objects.all()  # 所有布置的作业
    qs_all = User.objects.filter(user_type=1).order_by('student_id')
    qs_all_num = len(qs_all)
    return HttpResponse(template.render(locals()))

def issues(request, id):
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

    issue_num = range(1, Issue.objects.count() + 1)
    if id:
        issue = int(id)
    else:
        issue = Issue.objects.count()
        return HttpResponseRedirect('/teacher/issues/'+str(issue))
    time = timezone.now()
    permission = True
    template = get_template('teacher/issues.html')
    qi_all = Issue.objects.all()  # 所有布置的作业
    qi = Issue.objects.filter(id=issue)
    if qi:
        qi = qi[0]
    qs_not_all = User.objects.filter(user_type=1).exclude(homework__in=Homework.objects.filter(issue_id=issue, repo__isnull=False))\
        .values('student_id', 'github', 'name')
    for qs_not in qs_not_all:
        qh = Homework.objects.filter(issue_id=issue, student_id__student_id=qs_not['student_id'])
        if qh:
            qs_not['download_limit'] = qh[0].download_limit
    qh_has_all = Homework.objects.filter(issue_id=issue, repo__isnull=False)
    return HttpResponse(template.render(locals()))

################ 退出登录 ###################################
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

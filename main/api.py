# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue
from django.utils import timezone
import os, xlrd

################################## 学生操作 ################################################
# 更新学生姓名
def update_name(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    name = request.GET['name']
    user = request.user.username
    User.objects.filter(student_id=user).update(name=name)
    return HttpResponse('SUCCESS')

# 提交作业repo
def update_repo(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    repo = request.GET['repo']
    issue = request.GET['issue']
    user = request.user.username
    time = timezone.now()
    homework = Homework.objects.filter(student_id=user, issue_id=issue)
    if homework:
        homework.update(repo=repo, submit_time=time)
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('ERROR')
    
################################ 老师操作 #######################################################
# 作业下发，允许提交开关设置
def switch(request, target):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You are not log in.')

    # 查看是否是本课堂老师，不是则拒绝
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponse('Do not have the permission.')
    else:
        return HttpResponseRedirect('/')

    action = request.GET['action']
    issue = request.GET['issue']
    time = timezone.now()
    qi = Issue.objects.filter(id=issue)
    if qi:
        if target == 'switchissued':
            if action == 'open':
                qi.update(issued=True, allow_submit=True, issued_time=time)
            elif action=='close':
                qi.update(issued=False, allow_submit=False)
            else:
                return HttpResponse('The wrong action.')

        elif target == 'switchallowsubmit':
            if action == 'open':
                qi.update(allow_submit=True)
            elif action=='close':
                qi.update(allow_submit=False)
            else:
                return HttpResponse('The wrong action.')
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('ERROR')

# 文件上传
def upload_file(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You are not log in.')

    # 查看是否是本课堂老师，不是则拒绝
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponse('Do not have the permission.')
    else:
        return HttpResponseRedirect('/')

    if request.method == "POST":
        myFile =request.FILES.get("myfile", None)
        if not myFile:
            return HttpResponse("no files for upload!")

        baseDir = os.path.dirname(os.path.abspath(__name__))
        fileDir = os.path.join(baseDir,'tmp','upload')
        filename = os.path.join(fileDir, myFile.name)
        destination = open(filename, 'wb')  # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        data = xlrd.open_workbook(filename) # 打开xls文件
        table = data.sheets()[0] # 打开第一张表
        nrows = table.nrows # 获取表的行数
        for i in range(nrows):
            row_list = table.row_values(i)
            q = User.objects.filter(student_id=int(row_list[0]))
            if len(row_list) > 1:
                if q:
                    User.objects.filter(student_id=int(row_list[0])).update(name=row_list[1])
                else:
                    User.objects.create(student_id=int(row_list[0]), name=row_list[1], user_type=1)
            else:
                if not User.objects.filter(student_id=int(row_list[0])):
                    User.objects.create(student_id=int(row_list[0]), user_type=1)

        return HttpResponse("SUCCESS")  

def del_students(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You are not log in.')

    # 查看是否是本课堂老师，不是则拒绝
    user = request.user.username
    qu = User.objects.filter(student_id=user)
    if qu:
        if qu[0].user_type == 2:
            qu = qu[0]
        else:
            return HttpResponse('Do not have the permission.')
    else:
        return HttpResponseRedirect('/')

    del_id = request.GET['studentid']
    User.objects.filter(student_id=del_id).delete()
    return HttpResponse('SUCCESS')
    
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import xlrd
import json
import hashlib
import time
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue, Pending
from django.utils import timezone
from django.db.models import F
from django.core.files.storage import get_storage_class
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

################################## 学生操作 ################################################
# 学生更新姓名
def update_name(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    name = request.GET['name']
    user = request.user.username
    User.objects.filter(student_id=user).update(name=name)
    return HttpResponse('SUCCESS')

# 学生提交作业repo
def update_repo(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    repo = request.GET['repo']
    issue = request.GET['issue']
    user = request.user.username
    time = timezone.now()

    qh = Homework.objects.filter(student_id__student_id=user, issue_id=issue)
    qi = Issue.objects.filter(id=issue)

    # 当前作业是否存在
    if not qi:
        return HttpResponse('Issue is not issued.')

    # 学生还没有点击获取作业
    if not qh:
        return HttpResponse('Have not get the homework.')

    github = qh[0].student_id.github
    back = requests.get('https://api.github.com/repos/'+github+'/'+repo).text
    back = json.loads(back)
    if 'id' not in back:
        return HttpResponse('NOTEXIST')
    
    # 提交入口是否开启
    if qi[0].allow_submit:
        qh.update(repo=repo, submit_time=time)
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('Is not allowed to submit.')
        
# 下载实验环境
def get_environment(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    user = request.user.username
    issue = request.GET['issue']

    qh = Homework.objects.filter(student_id__student_id=user, issue_id=issue)

    # 判断是否是第一次获取作业
    if qh:
        if int(qh[0].download_limit) <= 0:
            return HttpResponse('Download times reach max value.')
        qh.update(download_limit=F('download_limit') - 1)
    else:
        Homework.objects.create(student_id=User.objects.get(student_id=user), download_limit=2, issue_id=issue)

    if issue != 1:
        baseDir = os.path.dirname(os.path.abspath(__name__))
        filename = 'lv'+issue+'-env.tar.gz'
        filepath = os.path.join(baseDir, 'tmp', 'experiments', 'lv'+issue)
        storge = get_storage_class()(filepath)
        respose = HttpResponse(storge.open(filename))
        respose['Content-Type'] = 'application/octet-stream'
        respose['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return respose

    # 生成实验环境...
    baseDir = os.path.dirname(os.path.abspath(__name__))
    os.system("sh "+baseDir+"/tmp/create_exp.sh " + user)
    # 返回作业
    filename = user + '_lv1.tar.gz'
    filepath = os.path.join(baseDir, 'tmp', 'experiments', 'lv1')
    storge = get_storage_class()(filepath)
    
    respose = HttpResponse(storge.open(filename))
    respose['Content-Type'] = 'application/octet-stream'
    respose['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return respose

################################ 老师操作 #######################################################
# 老师添加作业
def add_issue(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You have not logged in.')

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

    new_issue = Issue.objects.count()+1
    Issue.objects.create(id=new_issue,issued=True)
    return HttpResponseRedirect('/teacher/issues')

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

    # 该作业是否存在
    if not qi:
        return HttpResponse('Issue is not exist')

    # 如果执行的是下发作业开关
    if target == 'switchissued':
        if action == 'open':
            qi.update(issued=True, allow_submit=True, issued_time=time)
        elif action=='close':
            qi.update(issued=False, allow_submit=False)
        else:
            return HttpResponse('The wrong action.')

    # 如果执行的是提交入口开关
    elif target == 'switchallowsubmit':
        if action == 'open':
            qi.update(allow_submit=True)
        elif action=='close':
            qi.update(allow_submit=False)
        else:
            return HttpResponse('The wrong action.')
    else:
        return HttpResponse('The wrong target.')

    return HttpResponse('SUCCESS')

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

        # 保存文件
        baseDir = os.path.dirname(os.path.abspath(__name__))
        fileDir = os.path.join(baseDir,'tmp','upload')
        filename = os.path.join(fileDir, myFile.name)
        destination = open(filename, 'wb')  # 打开特定的文件进行二进制的写操作  
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        # 读取文件
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

# 老师删除学生
def del_students(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You have not logged in.')

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
    
# 老师增加学生
def add_student(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You have not logged in.')

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

    add_id = request.GET['studentid']
    add_name = request.GET['name']
    q = User.objects.filter(student_id=add_id)
    if q:
        if not q[0].name:
            q.update(name=add_name)
    else:
        User.objects.create(student_id=add_id, name=add_name)

    return HttpResponse('SUCCESS')

# 修改截止时间
def update_deadline(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('You do not log in.')

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

    issue = request.GET['issue']
    deadline = request.GET['deadline']
    qi = Issue.objects.filter(id=issue)
    if not qi:
        return HttpResponse('issue is not issued.')
    
    qi.update(deadline=deadline)
    return HttpResponse('SUCCESS')

######################### 作业检测 #####################################
# 学生作业检测
def check_request(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    user = request.user.username
    qu = User.objects.get(student_id=user)
    user_type = qu.user_type
    # 是老师返回
    if user_type == 2:
        return HttpResponse("This is a student's function.")
    
    issue = request.GET['issue']
    qh = Homework.objects.filter(student_id__student_id=user,issue_id=issue)
    if qh:
        qh = qh[0]
    else:
        return HttpResponse('Have not downloaded the homework.')
    # 检查是否绑定Github
    if qu.github:
        github = qu.github
    else:
        return HttpResponse('Have not binded Github.')
    # 检查是否提交作业
    if qh.repo:
        repo = qh.repo
    else:
        return HttpResponse('Have not submitted the homework.')

    homework_id = qh.id
    Homework.objects.filter(id=homework_id).update(self_check_result=3)
    Pending.objects.create(homework_id=homework_id, check_type=0)
    return HttpResponse('SUCCESS')

# 老师作业检测
def check_request_all(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponse('not login')

    user = request.user.username
    qu = User.objects.get(student_id=user)
    user_type = qu.user_type
    issue = request.GET['issue']
    time = timezone.now()
    # 是学生返回
    if user_type == 1:
        return HttpResponse("This is a teacher's function.")
    
    qh_all = Homework.objects.filter(issue_id=issue)
    qh_all_num = len(qh_all)
    qh_check_num = 0
    for qh in qh_all:
        # 检查是否提交作业
        if qh.repo:
            Homework.objects.filter(id=qh.id).update(check_result=3)
            Pending.objects.create(homework_id=qh.id, check_type=1)
            qh_check_num += 1
    Issue.objects.filter(id=issue).update(check_time=time)
    return HttpResponse('SUCCESS'+str(qh_all_num)+str(qh_check_num))

# 验收程序获取作业接口
@csrf_exempt
def get_check(request):
    if request.method == 'POST':
        stamp = int(request.POST['time'])
        current_time = int(time.time())

        # 时间600秒以外无效
        if current_time-stamp > 600:
            response_data= {
                'code': -101,
                'result': 'FAILED',
                'description': 'Time stamp check failed.'
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 
        
        # 验证签名
        sign = request.POST['sign']
        postdata = {
            'time': str(stamp)
        }
        args1 = json.dumps(postdata)  
        str1 = args1 + settings.SECRET_KEY  
        m = hashlib.md5()
        m.update(str1)  
        psw = m.hexdigest()
        if psw != sign:
            response_data= {
                'code': -100,
                'result': 'FAILED',
                'description': 'Sign check failed.'
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 

        pending_list = Pending.objects.filter(if_check=False).order_by('id')

        # 如果有待检测
        if pending_list:
            p = pending_list[0]
            check_id = p.id
            qh = Homework.objects.get(id=p.homework_id)
            github = qh.student_id.github
            repo = qh.repo
            issue = qh.issue_id
            response_data = {
                'code': 0,
                'check_id': check_id,
                'issue': issue,
                'github': github,
                'repo': repo
            }
            p.if_check = True
            p.save()
            return HttpResponse(json.dumps(response_data), content_type="application/json") 
        else:
            response_data= {
                'code': -1,
                'description': 'No homework pending.'
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 

# 验收程序返回结果
@csrf_exempt
def check_back(request):
    if request.method == 'POST':
        check_id = request.POST['check_id']
        result = request.POST['result']
        sign = request.POST['sign']
        
        # 验证签名
        postdata = {
            'check_id': check_id,
            'result': result
        }
        args1 = json.dumps(postdata)  
        str1 = args1 + settings.SECRET_KEY  
        m = hashlib.md5()
        m.update(str1)  
        psw = m.hexdigest()
        if psw != sign:
            response_data= {
                'code': -100,
                'result': 'FAILED',
                'description': 'Sign check failed.'
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 

        qp = Pending.objects.filter(id=check_id)
        # 如果该条存在
        if qp:
            qp = qp[0]
            homework_id = qp.homework_id
            check_type = qp.check_type
            # 学生自检
            if check_type == 0:
                Homework.objects.filter(id=homework_id).update(self_check_result=result)
            # 教师验收
            else:
                Homework.objects.filter(id=homework_id).update(check_result=result)
            qp.delete()

            response_data= {
                'code': 0,
                'result': 'SUCCESS',
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 
        
        # 如果该条不存在
        else:
            response_data= {
                'code': -2,
                'result': 'FAILED',
                'description': 'Check_id is not exist.'
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json") 
        
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue
from django.utils import timezone

# Create your views here.
def update_name(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    name = request.GET['name']
    user = request.user.username
    User.objects.filter(student_id=user).update(name=name)
    return HttpResponse('SUCCESS')

def update_repo(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

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
    

        


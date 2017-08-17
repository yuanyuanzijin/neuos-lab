# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User, Homework, Issue

# Create your views here.
def update_name(request):
    # 如果未登录则跳转到实验台
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    name = request.GET['name']
    user = request.user.username
    User.objects.filter(student_id=user).update(name=name)
    return HttpResponse('SUCCESS')

    

        


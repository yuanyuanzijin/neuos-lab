# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User

# Create your views here.
def index(request):
    template = get_template('login.html')
    return HttpResponse(template.render(locals()))

def home(request):
    # 如果用户未登录则返回首页
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    template = get_template('home.html')
    return HttpResponse(template.render(locals()))
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django_cas_ng import views as baseviews
from .models import User

# Create your views here.
def index(request):
    template = get_template('index.html')
    students = User.objects.all()
    student_lists = list()
    if request.user.is_authenticated():
        print request.user.get_username()
    else:
        print 'not login'

    return HttpResponse(template.render(locals()))

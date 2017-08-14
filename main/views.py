# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import User

# Create your views here.
def homepage(request):
    template = get_template('teacher.html')
    students = User.objects.all()
    student_lists = list()
    return HttpResponse(template.render(locals()))

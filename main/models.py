# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField
    studentid = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    github = models.CharField(max_length=20)
    permission = models.BooleanField

    class Meta:
        ordering = ('-studentid', )

    def __unicode__(self):
        return self.studentid

class Homework(models.Model):
    id_homework = models.AutoField
    studentid = models.CharField(max_length=10)
    issueid = models.CharField(max_length=10)
    download = models.CharField(max_length=10)
    repo = models.CharField(max_length=10)
    submit_time = models.DateTimeField
    self_check_result = models.BooleanField
    check_result = models.BooleanField

    class Meta:
        ordering = ('-studentid',)

    def __unicode__(self):
        return self.studentid

class Issue(models.Model):
    id_issue = models.AutoField
    issued = models.BooleanField
    url = models.URLField
    deadline = models.DateTimeField
    allow = models.BooleanField
    check_time = models.DateTimeField
    upload_percent = models.CharField(max_length=10)
    pass_percent = models.CharField(max_length=10)

    def __unicode__(self):
        return self.id_issue
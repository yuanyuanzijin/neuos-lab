# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField
    studentid = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    github = models.CharField(max_length=20)

    class Meta:
        ordering = ('-studentid', )

    def __unicode__(self):
        return self.studentid
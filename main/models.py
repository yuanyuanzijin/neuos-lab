# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):                           # id为默认序号，老师导入学生名单时建立此表
    studentid = models.CharField(max_length=10)     # 学号或职工号
    name = models.CharField(max_length=10, null=True, blank=True)          # 学生姓名
    github = models.CharField(max_length=30, null=True, blank=True)        # Github账号名称（用户名）
    permission = models.BooleanField(default=False)                # 是否具有教师权限

    class Meta:
        ordering = ('-studentid', )

    def __unicode__(self):
        return self.studentid

class Homework(models.Model):                       # id为作业生成顺序，每位同学第一次下载作业时建立此表
    studentid = models.CharField(max_length=10)     # 学号
    issueid = models.CharField(max_length=10)       # 作业序号（第几次序号）
    download = models.CharField(max_length=10, null=True)      # 下载次数
    repo = models.CharField(max_length=10, null=True)          # 提交的repo名称
    submit_time = models.DateTimeField(null=True)              # 提交时间
    self_check_result = models.CharField(max_length=10, null=True)         # 自检是否通过
    self_check_description = models.TextField(null=True)     # 自检结果描述
    check_result = models.CharField(max_length=10, null=True)              # 老师验收是否通过（最终结果评定）

    class Meta:
        ordering = ('-studentid',)

    def __unicode__(self):
        return self.studentid

class Issue(models.Model):                          # id为作业序号，方便以后扩展，此项目中只包含作业1
    issued = models.BooleanField(default=False)                    # 该作业是否被下发，老师第一次登录时点击下发按钮，才可以被下载
    url = models.URLField(null=True)                           # 实验环境获取地址，洋葱给出，手动填入
    deadline = models.DateTimeField(null=True)                 # 作业提交截止日期
    allow = models.BooleanField(default=False)                 # 老师点击下发作业之前或停止收取后，学生无法提交和验收作业，但可以查看结果
    check_time = models.DateTimeField(null=True)               # 老师批量验收的时间
    upload_percent = models.FloatField(null=True)              # 作业上交比例
    ontime_percent = models.FloatField(null=True)              # 作业按时上交比例
    pass_percent = models.CharField(max_length=10, null=True)  # 作业通过比例

    def __unicode__(self):
        return self.id
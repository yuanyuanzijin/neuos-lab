# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):                                                   # id为默认序号，老师导入学生名单时建立此表
    USER_TYPE_LIST = (
        (1, '学生'),
        (2, '老师'),
    )
    student_id = models.CharField(max_length=10)                            # 学号或职工号
    name = models.CharField(max_length=10, null=True, blank=True)           # 学生姓名
    github = models.CharField(max_length=30, null=True, blank=True)         # Github账号名称（用户名）
    user_type = models.IntegerField(default=1, choices=USER_TYPE_LIST)      # 是否具有教师权限
    create_at = models.DateTimeField(null=True, auto_now_add=True)          # 数据创建时间
    update_at = models.DateTimeField(null=True, auto_now=True)              # 数据更新时间

    class Meta:
        ordering = ('-student_id', )

    def __unicode__(self):
        return self.student_id


class Homework(models.Model):                                               # id为作业生成顺序，每位同学第一次下载作业时建立此表
    student_id = models.CharField(max_length=10)                            # 学号
    issue_id = models.CharField(max_length=10)                              # 作业序号（第几次序号）
    download_limit = models.CharField(max_length=10, null=True, blank=True)             # 下载次数
    repo = models.CharField(max_length=10, null=True, blank=True)                       # 提交的repo名称
    submit_time = models.DateTimeField(null=True, blank=True)                           # 提交时间
    check_result = models.CharField(max_length=10, null=True, blank=True)               # 作业检测结果
    create_at = models.DateTimeField(null=True, auto_now_add=True)          # 数据创建时间
    update_at = models.DateTimeField(null=True, auto_now=True)              # 数据更新时间

    class Meta:
        ordering = ('-student_id',)

    def __unicode__(self):
        return self.student_id


class Issue(models.Model):                                                              # id为作业序号，方便以后扩展，此项目中只包含作业1
    issued = models.BooleanField(default=False)                             # 该作业是否被下发，老师第一次登录时点击下发按钮，才可以被下载
    issued_time = models.DateTimeField(null=True, blank=True)
    request_url = models.URLField(null=True, blank=True)                                # 实验环境获取地址，洋葱给出，手动填入
    deadline = models.DateTimeField(null=True, blank=True)                              # 作业提交截止日期
    allow_submit = models.BooleanField(default=False)                       # 老师点击下发作业之前或停止收取后，学生无法提交和验收作业，但可以查看结果
    check_time = models.DateTimeField(null=True, blank=True)                            # 老师批量验收的时间
    create_at = models.DateTimeField(auto_now_add=True)          # 数据创建时间
    update_at = models.DateTimeField(auto_now=True)              # 数据更新时间

    def __unicode__(self):
        return str(self.id)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Homework, Issue

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'name', 'github', 'user_type', 'create_at', 'update_at')

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'issue_id', 'download_limit', 'repo', 'submit_time', 'check_result', \
                    'create_at', 'update_at')

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issued', 'request_url', 'deadline', 'allow_submit', 'check_time', 'create_at', 'update_at')

admin.site.register(User, UserAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Issue, IssueAdmin)
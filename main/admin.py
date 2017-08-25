# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Homework, Issue, Pending

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'name', 'github', 'user_type', 'create_at', 'update_at')

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'issue_id', 'download_limit', 'repo', 'submit_time', 'check_result', \
                    'create_at', 'update_at')

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issued', 'deadline', 'allow_submit', 'check_time', 'create_at', 'update_at')

class PendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'homework_id', 'check_type', 'create_at')

admin.site.register(User, UserAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Pending, PendingAdmin)
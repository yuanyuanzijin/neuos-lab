# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-17 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170817_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='permission',
        ),
        migrations.AddField(
            model_name='homework',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='issue',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, '\u5b66\u751f'), (2, '\u8001\u5e08')], default=1),
        ),
        migrations.AlterField(
            model_name='homework',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

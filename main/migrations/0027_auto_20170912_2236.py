# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 14:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_pending_if_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.User'),
        ),
    ]

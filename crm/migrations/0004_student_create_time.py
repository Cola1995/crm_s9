# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-07-29 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_userinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='create_time',
            field=models.DateField(blank=True, null=True, verbose_name='创建时间'),
        ),
    ]
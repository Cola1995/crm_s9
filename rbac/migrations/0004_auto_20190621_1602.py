# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-21 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_permission_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=32, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='rbac.Role', verbose_name='角色'),
        ),
    ]

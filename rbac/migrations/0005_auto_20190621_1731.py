# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-21 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_auto_20190621_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=255),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-06 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20180206_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='', null=True, upload_to='courses/%Y/%m', verbose_name='\u5c01\u9762\u56fe'),
        ),
    ]

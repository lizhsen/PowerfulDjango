# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-08 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_lesson_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='', max_length=100, verbose_name='\u8bbf\u95ee\u5730\u5740'),
        ),
    ]

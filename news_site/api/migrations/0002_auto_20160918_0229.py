# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='topic_name',
        ),
        migrations.AlterField(
            model_name='articleinfo',
            name='author',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='articleinfo',
            name='date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='articleinfo',
            name='image_url',
            field=models.URLField(blank=True, default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='articleinfo',
            name='video_url',
            field=models.URLField(blank=True, default=None, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='category_name',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]

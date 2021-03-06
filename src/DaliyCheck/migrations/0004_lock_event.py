# -*- coding: utf-8 -*-
# Generated by Django 1.10rc1 on 2016-12-27 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DaliyCheck', '0003_auto_20161025_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='lock_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_eventPID', models.CharField(blank=True, max_length=20, null=True)),
                ('_hostname', models.CharField(blank=True, max_length=40, null=True)),
                ('_resultPID', models.CharField(blank=True, max_length=20, null=True)),
                ('_timestamp', models.FloatField(blank=True, null=True)),
                ('_sql', models.CharField(blank=True, max_length=10000, null=True)),
            ],
            options={
                'ordering': ['_timestamp'],
            },
        ),
    ]

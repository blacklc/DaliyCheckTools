# -*- coding: utf-8 -*-
# Generated by Django 1.10rc1 on 2016-12-27 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DaliyCheck', '0006_ibmguardium'),
    ]

    operations = [
        migrations.CreateModel(
            name='NBU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_availStorageSpace', models.CharField(blank=True, max_length=20, null=True)),
                ('_availStorageSpaceInPercent', models.CharField(blank=True, max_length=20, null=True)),
                ('_usedStorageSpace', models.CharField(blank=True, max_length=20, null=True)),
                ('_usedStorageSpaceInPercent', models.CharField(blank=True, max_length=20, null=True)),
                ('_timestamp', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
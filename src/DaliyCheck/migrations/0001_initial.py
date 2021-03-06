# -*- coding: utf-8 -*-
# Generated by Django 1.10rc1 on 2016-10-19 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='check_Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_ip', models.CharField(blank=True, max_length=45, null=True)),
                ('_hostname', models.CharField(blank=True, max_length=100, null=True)),
                ('_avalaiblespace', models.IntegerField(blank=True, null=True)),
                ('_strogeused', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-_timestamp'],
            },
        ),
        migrations.CreateModel(
            name='date_timestamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_timestamp', models.FloatField(blank=True, null=True)),
                ('_date', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'ordering': ['-_timestamp'],
            },
        ),
        migrations.AddField(
            model_name='check_report',
            name='_timestamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DaliyCheck.date_timestamp'),
        ),
    ]

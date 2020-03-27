# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('acronym', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('rms_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('epa_id', models.CharField(max_length=32)),
                ('IRMS_project_id', models.CharField(max_length=32)),
                ('RMSprogram_id', models.IntegerField()),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('rms_id', models.IntegerField()),
                ('start_date', models.CharField(max_length=32, null=True, blank=True)),
                ('end_date', models.CharField(max_length=32, null=True, blank=True)),
                ('program', models.ForeignKey(to='rms.Program', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('epa_id', models.CharField(max_length=32)),
                ('RMSproject_id', models.IntegerField()),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('rms_id', models.IntegerField()),
                ('start_date', models.CharField(max_length=32, null=True, blank=True)),
                ('end_date', models.CharField(max_length=32, null=True, blank=True)),
                ('project', models.ForeignKey(to='rms.Project', on_delete=models.CASCADE)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notebooks_tab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotebooksTab_approval_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('modified', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('date_reviewed', models.DateField(db_index=True, null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('custodian', models.ForeignKey(on_delete=models.CASCADE, related_name='nbhist_contacts', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('nb_status', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab_Status', null=True)),
                ('nbtab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab', null=True)),
                ('qa_manager', models.ForeignKey(on_delete=models.CASCADE, related_name='nbhist_approving_managers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('supervisor_mentor', models.ForeignKey(on_delete=models.CASCADE, related_name='nbhist_supervisor_mentor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='nbhist_users', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]

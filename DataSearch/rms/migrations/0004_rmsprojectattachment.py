# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import rms.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rms', '0003_auto_20160707_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='RMSProjectAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('attachment', models.FileField(max_length=255, null=True, upload_to=rms.models.get_project_attachment_storage_path, blank=True)),
                ('file_name', models.CharField(max_length=255, null=True, blank=True)),
                ('file_size', models.CharField(max_length=255, null=True, blank=True)),
                ('created_by_user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='rms.Project', null=True)),
            ],
            options={
                'ordering': ['file_name'],
            },
        ),
    ]

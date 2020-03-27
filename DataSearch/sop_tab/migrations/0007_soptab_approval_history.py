# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sop_tab', '0006_soptab_sop_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOPTab_approval_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('modified', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('date_reviewed', models.DateField(db_index=True, null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('approving_manager', models.ForeignKey(on_delete=models.CASCADE, related_name='sophist_approving_managers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sop_contact', models.ForeignKey(on_delete=models.CASCADE, related_name='sophist_contacts', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('soptab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='sophist_users', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]

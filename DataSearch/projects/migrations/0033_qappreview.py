# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0032_auto_20170210_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='QAPPReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('date_email_sent', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('to_email_list', models.TextField(db_index=True, null=True, blank=True)),
                ('project', models.ForeignKey(to='projects.Project', on_delete=models.CASCADE, null=True)),
            ],
        ),
    ]

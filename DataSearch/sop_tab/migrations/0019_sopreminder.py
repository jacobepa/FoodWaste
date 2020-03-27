# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0018_auto_20170809_2308'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOPReminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('date_email_sent', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('to_email_list', models.TextField(db_index=True, null=True, blank=True)),
                ('soptab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab', null=True)),
            ],
        ),
    ]

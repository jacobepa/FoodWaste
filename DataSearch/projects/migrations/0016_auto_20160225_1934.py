# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20160216_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectlog',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='projectlog',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20170112_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='QAPPAnnualReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('date_email_sent', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('project', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='projects.Project', null=True)),
            ],
            options={
                'ordering': ['date_email_sent'],
            },
        ),
    ]

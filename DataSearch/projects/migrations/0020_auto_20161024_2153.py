# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20160819_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectlog',
            name='review_requested',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='participating_organizations',
            field=models.ManyToManyField(to='projects.ParticipatingOrganization'),
        ),
    ]

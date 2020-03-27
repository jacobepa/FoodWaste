# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0004_rmsprojectattachment'),
        ('projects', '0018_auto_20160323_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='rap_program',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='rap_program_projects', blank=True, to='rms.Program', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='rap_project',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='rap_project_projects', blank=True, to='rms.Project', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='rap_task',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='rap_task_projects', blank=True, to='rms.Task', null=True),
        ),
    ]

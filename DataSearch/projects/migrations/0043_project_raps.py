
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_project_suspend_reminder'),
    ]

    operations = [
        migrations.AddField(
            name='ace_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='ace_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='css_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='css_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='sswr_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='sswr_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='hhra_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='hhra_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='hsr_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='hsr_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='shc_rap_project_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        ),
        migrations.AddField(
            name='shc_rap_task_numbers',
            model_name='project',
            field=models.TextField(null=True, blank=True)
        )
    ]



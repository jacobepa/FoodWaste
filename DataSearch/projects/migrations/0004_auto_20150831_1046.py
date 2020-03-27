# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20150608_1513'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='project',
        #     name='nrmrl_qapp_requirement',
        # ),
        migrations.AddField(
            model_name='project',
            name='nrmrl_qapp_requirement',
            field=models.ManyToManyField(to='projects.NRMRLQAPPRequirement'),
        ),
    ]

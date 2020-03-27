# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0030_qappannualreview_to_email_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qappannualreview',
            name='project',
            field=models.ForeignKey(to='projects.Project', on_delete=models.CASCADE, null=True),
        ),
    ]

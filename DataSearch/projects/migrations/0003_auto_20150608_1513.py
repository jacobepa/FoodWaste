# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_office'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='qa_log_number',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]

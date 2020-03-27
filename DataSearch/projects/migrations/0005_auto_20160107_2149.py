# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20150831_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='qa_id',
            field=models.CharField(unique=True, max_length=255, blank=True),
        ),
    ]

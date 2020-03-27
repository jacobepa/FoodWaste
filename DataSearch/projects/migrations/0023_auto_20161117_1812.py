# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_auto_20161117_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='date_review_requested',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
    ]

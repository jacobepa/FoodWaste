# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0020_auto_20161024_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='review_requested',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
    ]

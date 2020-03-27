# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_lab_designation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='designation_code',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0024_auto_20170824_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='abbreviation',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='subdiscipline',
            name='abbreviation',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
    ]

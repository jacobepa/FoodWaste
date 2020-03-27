# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0023_remove_soptab_approving_manager_old'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='abbreviation',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='subdiscipline',
            name='abbreviation',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0005_soptab_sop_base_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='sop_version',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

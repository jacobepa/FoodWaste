# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0011_soptab_sop_base_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='previous_base_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]

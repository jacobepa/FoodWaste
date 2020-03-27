# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0025_auto_20170824_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab_approval_history',
            name='sop_status',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab_Status', null=True),
        ),
    ]

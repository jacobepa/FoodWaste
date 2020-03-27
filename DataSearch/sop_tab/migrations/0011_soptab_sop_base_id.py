# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0010_auto_20170719_0140'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='sop_base_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

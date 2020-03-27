# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0007_soptab_approval_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='comments',
            field=models.TextField(null=True, blank=True),
        ),
    ]

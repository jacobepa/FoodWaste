# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0013_soptab_approving_line_manager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soptab',
            options={'ordering': ['sop_base_id', 'sop_version'], 'get_latest_by': 'sop_version'},
        ),
        migrations.AddField(
            model_name='soptab',
            name='suspend_reminder',
            field=models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

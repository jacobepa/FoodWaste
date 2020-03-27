# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0019_sopreminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='is_current',
            field=models.CharField(default=b'Y', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

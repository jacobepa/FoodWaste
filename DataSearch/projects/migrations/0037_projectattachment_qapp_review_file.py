# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20170511_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectattachment',
            name='qapp_review_file',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

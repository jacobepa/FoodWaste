# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0015_discipline_subdiscipline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discipline',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='subdiscipline',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

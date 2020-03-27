# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20160323_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_epa_separation',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='display_in_dropdowns',
            field=models.CharField(default=b'Y', max_length=2, db_index=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

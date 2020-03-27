# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_auto_20170518_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='suspend_reminder',
            field=models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

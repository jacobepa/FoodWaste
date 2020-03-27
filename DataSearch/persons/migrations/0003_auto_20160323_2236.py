# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20160216_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='is_reviewer',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='personemergencycontact',
            name='share',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='personstatus',
            name='share',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

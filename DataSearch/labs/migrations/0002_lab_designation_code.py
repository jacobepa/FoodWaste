# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='designation_code',
            field=models.CharField(max_length=1, null=True, blank=True),
        ),
    ]

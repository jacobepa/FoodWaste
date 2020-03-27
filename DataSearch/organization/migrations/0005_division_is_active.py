# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20160218_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

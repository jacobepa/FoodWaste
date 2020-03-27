# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_auto_20170512_2348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectattachment',
            name='is_qapp_review_file',
        ),
    ]

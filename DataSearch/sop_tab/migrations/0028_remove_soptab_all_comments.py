# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0027_soptab_all_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soptab',
            name='all_comments',
        ),
    ]

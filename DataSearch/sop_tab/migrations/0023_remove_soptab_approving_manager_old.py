# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0022_auto_20170823_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soptab',
            name='approving_manager_old',
        ),
    ]

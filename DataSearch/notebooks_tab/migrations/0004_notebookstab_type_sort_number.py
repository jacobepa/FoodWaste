# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks_tab', '0003_auto_20171128_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebookstab_type',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

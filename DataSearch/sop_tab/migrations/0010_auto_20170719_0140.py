# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0009_auto_20170714_2224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soptab_status',
            options={'ordering': ['sort_number']},
        ),
        migrations.AddField(
            model_name='soptab_status',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='soptab',
            name='related_SOPs',
            field=models.ManyToManyField(related_name='related_SOPs_rel_+', to='sop_tab.SOPTab'),
        ),
    ]

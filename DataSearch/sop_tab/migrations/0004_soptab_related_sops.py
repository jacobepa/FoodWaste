# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0003_auto_20170630_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='related_SOPs',
            field=models.ManyToManyField(related_name='_soptab_related_SOPs_+', to='sop_tab.SOPTab'),
        ),
    ]

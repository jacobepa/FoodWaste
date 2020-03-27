# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0020_soptab_is_current'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soptabattachment',
            old_name='is_latest_SOP',
            new_name='is_latest_sop',
        ),
        migrations.RemoveField(
            model_name='soptab',
            name='related_SOPs',
        ),
        migrations.AddField(
            model_name='soptab',
            name='related_sops',
            field=models.ManyToManyField(related_name='_soptab_related_sops_+', to='sop_tab.SOPTab'),
        ),
    ]

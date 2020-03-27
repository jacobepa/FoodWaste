# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0017_auto_20170809_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='discipline',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.Discipline', null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='subdiscipline',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SubDiscipline', null=True),
        ),
    ]

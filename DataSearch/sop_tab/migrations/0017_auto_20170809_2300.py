# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0016_auto_20170809_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ['sort_number']},
        ),
        migrations.AlterModelOptions(
            name='subdiscipline',
            options={'ordering': ['sort_number']},
        ),
        migrations.AddField(
            model_name='discipline',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='subdiscipline',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20170511_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nrmrlqapprequirement',
            options={'ordering': ['sort_number']},
        ),
        migrations.AlterModelOptions(
            name='projecttype',
            options={'ordering': ['the_name']},
        ),
        migrations.RemoveField(
            model_name='projecttype',
            name='sort_number',
        ),
        migrations.AddField(
            model_name='nrmrlqapprequirement',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

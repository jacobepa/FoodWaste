# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_auto_20161117_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='programs',
            field=models.ManyToManyField(related_name='programs', to='projects.Program'),
        ),
        migrations.AlterField(
            model_name='project',
            name='program',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='program', blank=True, to='projects.Program', null=True),
        ),
    ]

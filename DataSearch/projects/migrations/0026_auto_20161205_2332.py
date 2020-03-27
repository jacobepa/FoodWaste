# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0025_auto_20161205_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='program',
        ),
        migrations.AlterField(
            model_name='project',
            name='programs',
            field=models.ManyToManyField(to='projects.Program'),
        ),
    ]

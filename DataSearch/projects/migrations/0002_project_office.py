# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='offices.Office', null=True),
        ),
    ]

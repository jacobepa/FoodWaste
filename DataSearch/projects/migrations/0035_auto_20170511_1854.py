# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_project_last_qapp_review_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projecttype',
            options={'ordering': ['sort_number']},
        ),
        migrations.AddField(
            model_name='projecttype',
            name='sort_number',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]

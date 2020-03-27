# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0033_qappreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='last_qapp_review_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]

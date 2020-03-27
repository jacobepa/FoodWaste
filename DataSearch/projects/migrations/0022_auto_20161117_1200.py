# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_auto_20161115_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectlog',
            old_name='review_requested',
            new_name='date_review_requested',
        ),
    ]

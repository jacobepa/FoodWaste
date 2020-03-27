# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0037_projectattachment_qapp_review_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectattachment',
            old_name='qapp_review_file',
            new_name='is_qapp_review_file',
        ),
    ]

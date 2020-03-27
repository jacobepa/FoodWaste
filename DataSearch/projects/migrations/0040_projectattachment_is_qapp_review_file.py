# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0039_remove_projectattachment_is_qapp_review_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectattachment',
            name='is_qapp_review_file',
            field=models.CharField(default=b'N', max_length=2, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

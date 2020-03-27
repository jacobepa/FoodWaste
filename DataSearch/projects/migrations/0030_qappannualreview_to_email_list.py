# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_qappannualreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='qappannualreview',
            name='to_email_list',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
    ]

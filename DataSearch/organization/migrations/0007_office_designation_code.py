# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_branch_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='office',
            name='designation_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]

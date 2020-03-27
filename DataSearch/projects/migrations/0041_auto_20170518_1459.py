# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_projectattachment_is_qapp_review_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='participatingorganization',
            name='agreement_number',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='participatingorganization',
            name='agreement_title',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]

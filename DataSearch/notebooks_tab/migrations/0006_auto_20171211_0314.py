# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks_tab', '0005_notebookstab_approval_history_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notebookstab',
            name='eNotebook_url',
            field=models.TextField(null=True, blank=True),
        ),
    ]

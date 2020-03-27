# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks_tab', '0004_notebookstab_type_sort_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='notebookstab_approval_history',
            name='status',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab_NotebookStatus', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20160107_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectattachment',
            name='attachment',
            field=models.FileField(max_length=255, null=True, upload_to=projects.models.get_project_attachment_storage_path, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20160216_2336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='epa_branch',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='collaborator_list',
            new_name='collaborators',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='epa_division',
            new_name='division',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='epa_lab',
            new_name='lab',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='epa_office',
            new_name='office',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_person',
            new_name='person',
        ),
    ]

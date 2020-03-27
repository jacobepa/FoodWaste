# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20160216_2337'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectlog',
            old_name='epa_branch',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='epa_division',
            new_name='division',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='epa_lab',
            new_name='lab',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='epa_office',
            new_name='office',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='log_reviewer',
            new_name='reviewer',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='tech_lead',
            new_name='technical_lead',
        ),
        migrations.RenameField(
            model_name='projectrequest',
            old_name='tech_lead',
            new_name='technical_lead',
        ),
    ]

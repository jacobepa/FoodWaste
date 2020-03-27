# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20160128_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participatingorganization',
            old_name='branch',
            new_name='branch_old',
        ),
        migrations.RenameField(
            model_name='participatingorganization',
            old_name='division',
            new_name='division_old',
        ),
        migrations.RenameField(
            model_name='participatingorganization',
            old_name='lab',
            new_name='lab_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='branch',
            new_name='branch_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='collaborators',
            new_name='collaborators_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='division',
            new_name='division_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='lab',
            new_name='lab_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='office',
            new_name='office_old',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='person',
            new_name='person_old',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='branch',
            new_name='branch_old',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='division',
            new_name='division_old',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='reviewer',
            new_name='reviewer_old',
        ),
        migrations.RenameField(
            model_name='projectlog',
            old_name='technical_lead',
            new_name='technical_lead_old',
        ),
        migrations.RenameField(
            model_name='projectrequest',
            old_name='technical_lead',
            new_name='technical_lead_old',
        ),
    ]

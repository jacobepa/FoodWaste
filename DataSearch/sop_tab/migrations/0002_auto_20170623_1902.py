# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_office_designation_code'),
        ('sop_tab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
        migrations.AlterField(
            model_name='soptab',
            name='alt_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='soptab',
            name='previous_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='soptab',
            name='sop_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]

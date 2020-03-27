# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_office_designation_code'),
        ('sop_tab', '0008_soptab_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='soptab',
            options={'ordering': ['sop_base_number', 'sop_version'], 'get_latest_by': 'sop_version'},
        ),
        migrations.AddField(
            model_name='soptab_orgs',
            name='branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
    ]

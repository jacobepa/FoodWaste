# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('projects', '0008_auto_20160216_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participatingorganization',
            old_name='office',
            new_name='epa_office',
        ),
        migrations.AddField(
            model_name='participatingorganization',
            name='epa_branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
        migrations.AddField(
            model_name='participatingorganization',
            name='epa_division',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True),
        ),
        migrations.AddField(
            model_name='participatingorganization',
            name='epa_lab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='epa_branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='epa_division',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='epa_lab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='epa_office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
        migrations.AddField(
            model_name='projectlog',
            name='epa_branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
        migrations.AddField(
            model_name='projectlog',
            name='epa_division',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True),
        ),
        migrations.AddField(
            model_name='projectlog',
            name='epa_lab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True),
        ),
        migrations.AddField(
            model_name='projectlog',
            name='epa_office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
    ]

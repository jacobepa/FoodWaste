# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('accounts', '0003_auto_20160130_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='branch',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='division',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
    ]

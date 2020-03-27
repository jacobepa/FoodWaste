# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160210_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestsubject',
            name='is_active',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='can_create_users',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='can_edit',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_reviewer',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_technical_lead',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

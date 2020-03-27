# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_auto_20160225_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nrmrlqapprequirement',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='program',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='qmp_required',
            field=models.CharField(blank=True, max_length=25, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectcategory',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectlog',
            name='is_finding_resolved',
            field=models.CharField(blank=True, max_length=25, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectlog',
            name='qa_view_required',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectlogtype',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='dqi_met',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='dqi_met_some',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='dqi_met_some_bad_data',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='dqi_na',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='was_qapp_prepared',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectrequest',
            name='was_qapp_required',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projectstatus',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='projecttype',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='qacategory',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='qappstatus',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='is_active',
            field=models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')]),
        ),
    ]

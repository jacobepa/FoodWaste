# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import sop_tab.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sop_tab', '0002_auto_20170623_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOPTabAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(max_length=255, null=True, upload_to=sop_tab.models.get_soptab_attachment_storage_path, blank=True)),
                ('include_in_email', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('is_review_file', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('is_latest_SOP', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('the_size', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.CreateModel(
            name='SOPTabReviewDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['modified'],
            },
        ),
        migrations.AddField(
            model_name='soptab',
            name='date_effective',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_number_x',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_number_y',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='soptabreviewdistribution',
            name='soptab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab', null=True),
        ),
        migrations.AddField(
            model_name='soptabreviewdistribution',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='soptabattachment',
            name='soptab',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_attachments', blank=True, to='sop_tab.SOPTab', null=True),
        ),
        migrations.AddField(
            model_name='soptabattachment',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

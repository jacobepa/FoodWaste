# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import branches.models


class Migration(migrations.Migration):

    dependencies = [
        ('immediate_offices', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offices', '0001_initial'),
        ('labs', '0001_initial'),
        ('divisions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=branches.models.get_branch_path, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('abbreviation', models.CharField(max_length=15, null=True, blank=True)),
                ('weblink', models.CharField(max_length=255, null=True, blank=True)),
                ('ordering', models.DecimalField(null=True, max_digits=10, decimal_places=1, blank=True)),
                ('the_description', models.TextField(null=True, blank=True)),
                ('division', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='divisions.Division', null=True)),
                ('immediate_office', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='immediate_offices.ImmediateOffice', null=True)),
                ('lab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='labs.Lab', null=True)),
                ('office', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='offices.Office', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

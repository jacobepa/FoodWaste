# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import labs.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=labs.models.get_lab_path, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('abbreviation', models.CharField(max_length=15, null=True, blank=True)),
                ('weblink', models.CharField(max_length=255, null=True, blank=True)),
                ('ordering', models.DecimalField(null=True, max_digits=10, decimal_places=1, blank=True)),
                ('the_description', models.TextField(null=True, blank=True)),
                ('office', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='offices.Office', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['abbreviation'],
            },
        ),
    ]

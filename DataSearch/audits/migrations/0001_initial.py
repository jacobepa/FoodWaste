# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('abbreviation', models.CharField(max_length=15, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Y'), (b'N', b'N')])),
                ('weblink', models.CharField(max_length=255, null=True, blank=True)),
                ('ordering', models.DecimalField(null=True, max_digits=10, decimal_places=1, blank=True)),
                ('the_description', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

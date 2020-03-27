# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notebooks_tab', '0002_notebookstab_approval_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotebooksTab_NotebookStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('sort_number', models.IntegerField(null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='status',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab_NotebookStatus', null=True),
        ),
    ]

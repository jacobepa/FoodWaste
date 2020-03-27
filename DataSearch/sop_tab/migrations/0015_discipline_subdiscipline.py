# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sop_tab', '0014_auto_20170801_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discipline', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubDiscipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subdiscipline', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('description', models.TextField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('discipline', models.ForeignKey(to='sop_tab.Discipline', on_delete=models.CASCADE)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('division', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=32)),
                ('url', models.CharField(max_length=1024, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='lab',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Office'),
        ),
        migrations.AddField(
            model_name='division',
            name='lab',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Lab'),
        ),
        migrations.AddField(
            model_name='division',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Office'),
        ),
        migrations.AddField(
            model_name='branch',
            name='division',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Division'),
        ),
        migrations.AddField(
            model_name='branch',
            name='lab',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Lab'),
        ),
        migrations.AddField(
            model_name='branch',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, to='organization.Office'),
        ),
    ]

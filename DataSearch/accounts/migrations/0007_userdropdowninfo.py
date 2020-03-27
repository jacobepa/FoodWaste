# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20171030_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDropdownInfo',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, blank=True)),
                ('email', models.CharField(max_length=254, null=True, blank=True)),
            ],
            options={
                'db_table': 'app_user_dropdown',
                'managed': False,
            },
        ),
    ]

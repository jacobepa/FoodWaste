# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sop_tab', '0021_auto_20170817_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='soptab',
            name='approving_manager_old',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_approving_managers', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='soptab',
            name='approving_manager',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_approvers', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

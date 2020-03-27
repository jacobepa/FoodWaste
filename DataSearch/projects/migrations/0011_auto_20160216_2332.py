# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0010_projectrequest_tech_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectlog',
            name='log_reviewer',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='projectlog_reviewer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='projectlog',
            name='tech_lead',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='projectlog_tech_lead', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

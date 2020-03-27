# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0009_auto_20160216_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectrequest',
            name='tech_lead',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='projectrequest_tech_lead', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('projects', '0007_auto_20160216_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='participatingorganization',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='project_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

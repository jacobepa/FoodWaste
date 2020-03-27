# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0011_auto_20160216_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='collaborator_list',
            field=models.ManyToManyField(related_name='project_collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='project_person',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='project_person', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

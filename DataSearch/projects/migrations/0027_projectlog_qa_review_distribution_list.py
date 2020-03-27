# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0026_auto_20161205_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectlog',
            name='qa_review_distribution_list',
            field=models.ManyToManyField(related_name='qa_review_distribution_lis', to=settings.AUTH_USER_MODEL),
        ),
    ]

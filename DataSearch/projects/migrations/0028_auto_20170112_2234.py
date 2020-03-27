# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0027_projectlog_qa_review_distribution_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectlog',
            name='qa_review_distribution_list',
            field=models.ManyToManyField(related_name='qa_review_distribution_list', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

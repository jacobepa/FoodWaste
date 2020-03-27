# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_auto_20170209_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qappannualreview',
            name='project',
        ),
        migrations.DeleteModel(
            name='QAPPAnnualReview',
        ),
    ]

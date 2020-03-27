# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_auto_20160323_2236'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectlog',
            old_name='qa_view_required',
            new_name='qa_review_required',
        ),
    ]

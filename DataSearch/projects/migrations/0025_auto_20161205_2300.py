# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_many_programs(apps, schema_editor):
    """
        Adds the Program object in Project.program to the
        many-to-many relationship in Project.programs
    """
    Project = apps.get_model('projects', 'Project')

    for project in Project.objects.all():
        if project.program is not None:
            project.programs.add(project.program)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0024_auto_20161205_2259'),
    ]

    operations = [
        migrations.RunPython(make_many_programs),
    ]

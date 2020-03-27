# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0041_auto_20170518_1459'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0007_office_designation_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOPTab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('modified', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('sop_number', models.CharField(max_length=255, blank=True)),
                ('alt_id', models.CharField(max_length=255, blank=True)),
                ('full_title', models.TextField(null=True, blank=True)),
                ('date_approved', models.DateField(db_index=True, null=True, blank=True)),
                ('date_reviewed', models.DateField(db_index=True, null=True, blank=True)),
                ('date_last_revision', models.DateField(db_index=True, null=True, blank=True)),
                ('keywords', models.TextField(null=True, blank=True)),
                ('previous_id', models.CharField(max_length=255, blank=True)),
                ('sop_review_email_list', models.TextField(db_index=True, null=True, blank=True)),
                ('the_description', models.TextField(null=True, blank=True)),
                ('approving_manager', models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_approving_managers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('division', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True)),
                ('lab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True)),
            ],
            options={
                'ordering': ['sop_number'],
            },
        ),
        migrations.CreateModel(
            name='SOPTab_MuralType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.CreateModel(
            name='SOPTab_Orgs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('division', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True)),
                ('lab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True)),
                ('office', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True)),
                ('soptab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab', null=True)),
            ],
            options={
                'ordering': ['soptab_id'],
            },
        ),
        migrations.CreateModel(
            name='SOPTab_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.CreateModel(
            name='SOPTab_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.AddField(
            model_name='soptab',
            name='mural_type',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab_MuralType', null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='participating_orgs',
            field=models.ManyToManyField(to='projects.ParticipatingOrganization'),
        ),
        migrations.AddField(
            model_name='soptab',
            name='programs',
            field=models.ManyToManyField(to='projects.Program'),
        ),
        migrations.AddField(
            model_name='soptab',
            name='projects',
            field=models.ManyToManyField(to='projects.Project'),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_contact',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_contacts', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_review_distribution_list',
            field=models.ManyToManyField(related_name='soptabs_review_distribution_list', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_status',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab_Status', null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='sop_type',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='sop_tab.SOPTab_Type', null=True),
        ),
        migrations.AddField(
            model_name='soptab',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='soptab_users', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

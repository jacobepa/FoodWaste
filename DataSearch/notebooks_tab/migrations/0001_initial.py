# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import notebooks_tab.models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_office_designation_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0042_project_suspend_reminder'),
    ]

    operations = [
        migrations.CreateModel(
            name='NBReminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('date_email_sent', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('to_email_list', models.TextField(db_index=True, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotebooksTab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('modified', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('previous_id', models.CharField(max_length=255, null=True, blank=True)),
                ('nb_number', models.CharField(max_length=255, null=True, blank=True)),
                ('alt_id', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('non_ord_contributors', models.TextField(db_index=True, null=True, blank=True)),
                ('nb_review_email_list', models.TextField(db_index=True, null=True, blank=True)),
                ('eNotebook_url', models.CharField(max_length=255, null=True, blank=True)),
                ('date_issued', models.DateField(db_index=True, null=True, blank=True)),
                ('date_reviewed', models.DateField(db_index=True, null=True, blank=True)),
                ('date_final_use', models.DateField(db_index=True, null=True, blank=True)),
                ('date_archived', models.DateField(db_index=True, null=True, blank=True)),
                ('comments', models.TextField(null=True, blank=True)),
                ('schedule_review', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('branch', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True)),
                ('custodian', models.ForeignKey(on_delete=models.CASCADE, related_name='nb_custodians', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('division', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True)),
                ('lab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True)),
                ('nb_review_distribution_list', models.ManyToManyField(related_name='nb_review_distribution_list', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotebooksTab_Orgs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('branch', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Branch', null=True)),
                ('division', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Division', null=True)),
                ('lab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Lab', null=True)),
                ('nbtab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab', null=True)),
                ('office', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True)),
            ],
            options={
                'ordering': ['nbtab_id'],
            },
        ),
        migrations.CreateModel(
            name='NotebooksTab_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.CharField(blank=True, max_length=4, null=True, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('sort_number', models.IntegerField(null=True, blank=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['sort_number'],
            },
        ),
        migrations.CreateModel(
            name='NotebooksTab_Type',
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
            name='NotebooksTabAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(max_length=255, null=True, upload_to=notebooks_tab.models.get_nbtab_attachment_storage_path, blank=True)),
                ('include_in_email', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('is_review_file', models.CharField(default=b'N', max_length=4, choices=[(b'', b''), (b'Y', b'Yes'), (b'N', b'No')])),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('the_size', models.CharField(max_length=255, null=True, blank=True)),
                ('nbtab', models.ForeignKey(on_delete=models.CASCADE, related_name='nbtab_attachments', blank=True, to='notebooks_tab.NotebooksTab', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.CreateModel(
            name='NotebooksTabReviewDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.TextField(null=True, blank=True)),
                ('nbtab', models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab', null=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['modified'],
            },
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='nb_status',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab_Status', null=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='nb_type',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab_Type', null=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='office',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='organization.Office', null=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='ord_contributors',
            field=models.ManyToManyField(related_name='nb_ord_contributors', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='participating_orgs',
            field=models.ManyToManyField(to='projects.ParticipatingOrganization'),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='programs',
            field=models.ManyToManyField(to='projects.Program'),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='projects',
            field=models.ManyToManyField(to='projects.Project'),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='qa_manager',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='nbtab_qa_managers', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='supervisor_mentor',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='nbtab_supervisors', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='notebookstab',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='nbtab_users', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='nbreminder',
            name='nbtab',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='notebooks_tab.NotebooksTab', null=True),
        ),
    ]

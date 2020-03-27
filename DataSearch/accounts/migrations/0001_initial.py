# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=accounts.models.get_contact_request_path, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('email_address', models.CharField(max_length=255, null=True, blank=True)),
                ('greenscope_response', models.CharField(max_length=255, null=True, blank=True)),
                ('response_date', models.DateField(null=True, blank=True)),
                ('the_description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('the_name', models.CharField(max_length=255, null=True, blank=True)),
                ('email_address', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True, blank=True)),
                ('last_modified_by', models.CharField(max_length=255, null=True, blank=True)),
                ('attachment', models.FileField(null=True, upload_to=accounts.models.get_profile_photo_storage_path, blank=True)),
                ('user_type', models.CharField(blank=True, max_length=45, null=True, choices=[(b'SUPER', b'SUPER USER'), (b'OFFICE', b'OFFICE'), (b'ALL', b'ALL LABS'), (b'LAB', b'SINGLE LAB'), (b'DIVISION', b'DIVISION USER'), (b'BRANCH', b'BRANCH USER')])),
                ('code_kept', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, blank=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('telephone', models.CharField(max_length=30, null=True, blank=True)),
                ('telephone_extension', models.CharField(max_length=30, null=True, blank=True)),
                ('user_lab_one', models.CharField(max_length=45, null=True, blank=True)),
                ('user_division_one', models.CharField(max_length=45, null=True, blank=True)),
                ('user_branch_one', models.CharField(max_length=45, null=True, blank=True)),
                ('mail_to_name', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('mail_to_address', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_to_city', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_to_state', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_to_zipcode', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_to_mailstop', models.CharField(max_length=255, null=True, blank=True)),
                ('mail_to_note', models.CharField(max_length=255, null=True, blank=True)),
                ('company', models.CharField(max_length=255, null=True, blank=True)),
                ('email_address_epa', models.CharField(max_length=255, null=True, blank=True)),
                ('email_address_other', models.CharField(max_length=255, null=True, blank=True)),
                ('is_reviewer', models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Y'), (b'N', b'N')])),
                ('is_technical_lead', models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Y'), (b'N', b'N')])),
                ('can_edit', models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Y'), (b'N', b'N')])),
                ('can_create_users', models.CharField(blank=True, max_length=5, null=True, choices=[(b'', b''), (b'Y', b'Y'), (b'N', b'N')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='request_subject',
            field=models.ForeignKey(on_delete=models.CASCADE, blank=True, to='accounts.RequestSubject', null=True),
        ),
    ]

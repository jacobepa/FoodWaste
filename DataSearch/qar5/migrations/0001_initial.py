# Generated by Django 3.0.4 on 2020-04-10 15:08

import constants.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Qapp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('division_branch', models.TextField()),
                ('title', models.TextField()),
                ('qa_category', models.TextField()),
                ('intra_extra', models.CharField(max_length=64)),
                ('revision_number', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('strap', models.TextField()),
                ('tracking_id', models.TextField()),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='divisions', to='qar5.Division')),
                ('prepared_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QappApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_plan_title', models.TextField()),
                ('activity_number', models.TextField()),
                ('qapp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='qar5.Qapp')),
            ],
        ),
        migrations.CreateModel(
            name='SectionBType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='References',
            fields=[
                ('qapp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='qar5.Qapp')),
                ('references', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SectionA',
            fields=[
                ('qapp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='qar5.Qapp')),
                ('a2', models.TextField()),
                ('a3', models.TextField()),
                ('a4', models.TextField()),
                ('a4_chart', models.FileField(blank=True, null=True, upload_to=constants.utils.get_attachment_storage_path)),
                ('a5', models.TextField()),
                ('a6', models.TextField()),
                ('a7', models.TextField()),
                ('a8', models.TextField()),
                ('a9', models.TextField()),
                ('a9_drive_path', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SectionC',
            fields=[
                ('qapp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='qar5.Qapp')),
            ],
        ),
        migrations.CreateModel(
            name='SectionD',
            fields=[
                ('qapp', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='qar5.Qapp')),
                ('d1', models.TextField()),
                ('d2', models.TextField()),
                ('d3', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.TextField()),
                ('description', models.TextField()),
                ('effective_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('initial_version', models.TextField()),
                ('qapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.Qapp')),
            ],
        ),
        migrations.CreateModel(
            name='QappSharingTeamMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('can_edit', models.BooleanField(default=True)),
                ('qapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qapp_teams', to='qar5.Qapp')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_qapp', to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='QappLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('qapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.Qapp')),
            ],
        ),
        migrations.CreateModel(
            name='QappApprovalSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractor', models.BooleanField(blank=True, default=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('signature', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
                ('qapp_approval', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.QappApproval')),
            ],
        ),
        migrations.AddField(
            model_name='qapp',
            name='teams',
            field=models.ManyToManyField(through='qar5.QappSharingTeamMap', to='teams.Team'),
        ),
        migrations.CreateModel(
            name='SectionBTypeMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionb_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.SectionBType')),
                ('sectiona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.SectionA')),
            ],
        ),
        migrations.CreateModel(
            name='SectionB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b1_1', models.TextField(blank=True, null=True)),
                ('b1_2', models.TextField(blank=True, null=True)),
                ('b1_3', models.TextField(blank=True, null=True)),
                ('b1_4', models.TextField(blank=True, null=True)),
                ('b1_5', models.TextField(blank=True, null=True)),
                ('b2_1', models.TextField(blank=True, null=True)),
                ('b2_2', models.TextField(blank=True, null=True)),
                ('b2_3', models.TextField(blank=True, null=True)),
                ('b2_4', models.TextField(blank=True, null=True)),
                ('b2_5', models.TextField(blank=True, null=True)),
                ('b2_6', models.TextField(blank=True, null=True)),
                ('b2_7', models.TextField(blank=True, null=True)),
                ('b2_8', models.TextField(blank=True, null=True)),
                ('b3_1', models.TextField(blank=True, null=True)),
                ('b3_2', models.TextField(blank=True, null=True)),
                ('b3_3', models.TextField(blank=True, null=True)),
                ('b3_4', models.TextField(blank=True, null=True)),
                ('b3_5', models.TextField(blank=True, null=True)),
                ('b3_6', models.TextField(blank=True, null=True)),
                ('b3_7', models.TextField(blank=True, null=True)),
                ('b3_8', models.TextField(blank=True, null=True)),
                ('b3_9', models.TextField(blank=True, null=True)),
                ('b3_10', models.TextField(blank=True, null=True)),
                ('b4_1', models.TextField(blank=True, null=True)),
                ('b4_2', models.TextField(blank=True, null=True)),
                ('b4_3', models.TextField(blank=True, null=True)),
                ('b4_4', models.TextField(blank=True, null=True)),
                ('b4_5', models.TextField(blank=True, null=True)),
                ('b5_1', models.TextField(blank=True, null=True)),
                ('b5_2', models.TextField(blank=True, null=True)),
                ('b6_1', models.TextField(blank=True, null=True)),
                ('b6_2', models.TextField(blank=True, null=True)),
                ('qapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.Qapp')),
                ('sectionb_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qar5.SectionBType')),
            ],
            options={
                'unique_together': {('qapp', 'sectionb_type')},
            },
        ),
        migrations.AddField(
            model_name='sectiona',
            name='sectionb_type',
            field=models.ManyToManyField(through='qar5.SectionBTypeMap', to='qar5.SectionBType'),
        ),
    ]

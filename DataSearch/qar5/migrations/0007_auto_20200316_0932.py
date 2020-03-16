# Generated by Django 3.0.3 on 2020-03-16 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('qar5', '0006_auto_20200220_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='QappSharingTeamMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('can_edit', models.BooleanField()),
                ('qapp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qapp_teams', to='qar5.Qapp')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_qapp', to='teams.Team')),
            ],
        ),
        migrations.AddField(
            model_name='qapp',
            name='teams',
            field=models.ManyToManyField(through='qar5.QappSharingTeamMap', to='teams.Team'),
        ),
    ]

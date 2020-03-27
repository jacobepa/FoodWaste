# Generated by Django 2.2.3 on 2019-10-09 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0061_auto_20190915_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtramuralVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('last_modified_by', models.CharField(blank=True, max_length=255, null=True)),
                ('the_name', models.CharField(blank=True, max_length=255, null=True)),
                ('institution_name', models.CharField(blank=True, max_length=255, null=True)),
                ('vehicle_number', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.CharField(blank=True, choices=[('', ''), ('Y', 'Yes'), ('N', 'No')], max_length=4, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.VehicleType')),
            ],
            options={
                'ordering': ['the_name'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='extramural_vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.ExtramuralVehicle'),
        ),
    ]

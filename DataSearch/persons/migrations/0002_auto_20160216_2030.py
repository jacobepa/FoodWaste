# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresstype',
            name='user',
        ),
        migrations.RemoveField(
            model_name='emailtype',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personaddress',
            name='address_type',
        ),
        migrations.RemoveField(
            model_name='personaddress',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personaddress',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personattachment',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personattachment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='persondivisionbranch',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='persondivisionbranch',
            name='division',
        ),
        migrations.RemoveField(
            model_name='persondivisionbranch',
            name='person',
        ),
        migrations.RemoveField(
            model_name='persondivisionbranch',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personemail',
            name='email_type',
        ),
        migrations.RemoveField(
            model_name='personemail',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personemail',
            name='user',
        ),
        migrations.RemoveField(
            model_name='personphone',
            name='person',
        ),
        migrations.RemoveField(
            model_name='personphone',
            name='phone_type',
        ),
        migrations.RemoveField(
            model_name='personphone',
            name='user',
        ),
        migrations.RemoveField(
            model_name='phonetype',
            name='user',
        ),
        migrations.DeleteModel(
            name='AddressType',
        ),
        migrations.DeleteModel(
            name='EmailType',
        ),
        migrations.DeleteModel(
            name='PersonAddress',
        ),
        migrations.DeleteModel(
            name='PersonAttachment',
        ),
        migrations.DeleteModel(
            name='PersonDivisionBranch',
        ),
        migrations.DeleteModel(
            name='PersonEmail',
        ),
        migrations.DeleteModel(
            name='PersonPhone',
        ),
        migrations.DeleteModel(
            name='PhoneType',
        ),
    ]

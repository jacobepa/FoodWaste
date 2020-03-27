# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.postgres.fields import ArrayField
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks_tab', '0007_auto_20180406_1916'),
    ]

    review_sql = """
        CREATE OR REPLACE VIEW notebooks_tab_notebookstab_recent_reviews as (
            with reviews as (
                select row_number() over (partition by r.user_id order by r.date_reviewed desc nulls last) as review_order, * from notebooks_tab_notebookstab_reviews r
            )
            select row_number() OVER (ORDER BY user_id) AS id, id as review_id, nbtab_id, status_id, user_id, date_reviewed from reviews where review_order = 1
        );

    """

    email_sql = """
        CREATE OR REPLACE VIEW notebooks_tab_notebookstab_recent_emails as (
            with emails as (
                select row_number() over (partition by sr.user_id order by sr.email_last_sent desc nulls last) as email_order, * from notebooks_tab_notebookstab_schedule_review sr
            )
            select row_number() OVER (ORDER BY user_id) AS id, id as review_id, nbtab_id, user_id, email_last_sent from emails where email_order = 1
        );
    """

    user_nb_sql = """
        CREATE OR REPLACE VIEW notebooks_tab_notebookstab_user_notebooks as (
         WITH custodians AS (
                 SELECT notebooks_tab_notebookstab.custodian_id AS user_id,
                    notebooks_tab_notebookstab.id AS notebookstab_id
                   FROM notebooks_tab_notebookstab
                  WHERE notebooks_tab_notebookstab.custodian_id IS NOT NULL
                ), contributors AS (
                 SELECT c.user_id, c.notebookstab_id
                   FROM notebooks_tab_notebookstab_ord_contributors c
                ), notebook_users AS (
                 SELECT 'custodian'::text AS role,
                    custodians.user_id,
                    custodians.notebookstab_id
                   FROM custodians
                UNION ALL
                 SELECT 'contributor'::text AS role,
                    contributors.user_id,
                    contributors.notebookstab_id
                   FROM contributors
                )
         SELECT row_number() OVER (ORDER BY u.user_id) AS id,
            u.user_id,
            array_agg(nb.id) AS nbtab_ids,
            array_agg(u.role) AS roles,
            array_agg(r.id) AS review_ids,
            rr.id as recent_review_id,
            re.id as recent_email_id
           FROM notebook_users u
             LEFT JOIN notebooks_tab_notebookstab nb ON nb.id = u.notebookstab_id
             LEFT JOIN notebooks_tab_notebookstab_reviews r ON r.user_id = u.user_id AND r.nbtab_id = nb.id
             LEFT JOIN notebooks_tab_notebookstab_recent_reviews rr on rr.user_id = u.user_id
             LEFT JOIN notebooks_tab_notebookstab_recent_emails re on re.user_id = u.user_id
             group by u.user_id, rr.date_reviewed, rr.id, re.id
        );
    """


    operations = [
        migrations.CreateModel(
            name='NotebooksTab_Reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nbtab', models.ForeignKey(blank=True, to='notebooks_tab.NotebooksTab', null=True, on_delete=models.CASCADE)),
                ('status', models.ForeignKey(blank=True, to='notebooks_tab.NotebooksTab_Status', null=True, on_delete=models.CASCADE)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('created', models.DateField(default=datetime.datetime.now, null=True, blank=True)),
                ('date_reviewed', models.DateField(null=True, blank=True, db_index=True)),
            ],
            options={
                'ordering': ['nbtab_id'],
            },
        ),
        migrations.CreateModel(
            name='NotebooksTab_Schedule_Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_review', models.CharField(blank=True, default='N', max_length=2)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('nbtab', models.ForeignKey(blank=False, null=False, on_delete=models.deletion.CASCADE, to='notebooks_tab.NotebooksTab')),
                ('email_last_sent', models.DateField(null=True, blank=True, db_index=True)),
            ],
        ),

        migrations.RunSQL(review_sql, reverse_sql="DROP VIEW IF EXISTS notebooks_tab_notebookstab_recent_reviews CASCADE ;"),
        migrations.RunSQL(email_sql, reverse_sql="DROP VIEW IF EXISTS notebooks_tab_notebookstab_recent_emails CASCADE ;"),
        migrations.RunSQL(user_nb_sql, reverse_sql="DROP VIEW IF EXISTS notebooks_tab_notebookstab_user_notebooks;"),
    ]

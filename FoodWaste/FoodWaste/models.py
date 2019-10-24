# models.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of models."""

from constants.models import YES_OR_NO
from django.db import models
from django.utils import timezone
#from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Team, User

def get_attachment_storage_path(instance, filename):
    """Build the attachment storage path using username and filename"""
    return '%s/attachments/%s' % (instance.uploaded_by.username, filename)


class Attachment(models.Model):
    """Class representing a file attachment to an Existing Data entry"""
    name = models.CharField(blank=False, null=False, max_length=255)
    file = models.FileField(null=True, blank=True, upload_to=get_attachment_storage_path)
    uploaded_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)


class SecondaryExistingData(models.Model):
    """Class representing an instance of Secondary / Existing Data Tracking Tool."""

    work = models.CharField(blank=False, null=False, max_length=255)
    email = models.CharField(blank=False, null=False, max_length=255)
    #phone = PhoneNumberField(blank=False, null=False)
    phone = models.CharField(blank=False, null=False, max_length = 32)
    search = models.CharField(blank=False, null=False, max_length=255)
    article_title = models.CharField(blank=False, null=False, max_length=255)

    # indicates if EPA disclaimer should be included when printing/exporting this data
    disclaimer_req = models.BooleanField(blank=False)

    citation = models.CharField(blank=False, null=False, max_length=512)
    date_accessed = models.DateTimeField(blank=False, null=False, default=timezone.now)
    comments = models.CharField(blank=True, null=True, max_length=512)
    created_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    # List of teams with which the Secondary Data is shared.
    teams = models.ManyToManyField(Team, through='SecondaryDataSharingTeamMap')
    attachments = models.ManyToManyField(Attachment, through='DataAttachmentMap')


class DataAttachmentMap(models.Model):
    """Mapping between Secondary / Existing Data and uploaded attachments"""

    data = models.ForeignKey(SecondaryExistingData, blank=False,
                             related_name='secondary_data_attachments',
                             on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, blank=False,
                                   related_name='attachment_secondary_data',
                                   on_delete=models.CASCADE)


class SecondaryDataSharingTeamMap(models.Model):
    """
    Mapping between Secondary/Existing Data and the Teams
    with which they are shared.
    """

    added_date = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    data = models.ForeignKey(SecondaryExistingData, blank=False,
                             related_name='secondary_data_teams',
                             on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=False,
                             related_name='team_secondary_data',
                             on_delete=models.CASCADE)
    # indicates if the team can edit the project
    can_edit = models.BooleanField(blank=False)

# models.py (DataSearch)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,E1101,W0611,C0411


"""Definition of models."""

from django.db import models
from django.utils import timezone
from teams.models import Team, User


def get_attachment_storage_path(instance, filename):
    """Build the attachment storage path using username and filename."""
    return 'uploads/%s/attachments/%s' % (instance.uploaded_by.username, filename)


class Division(models.Model):
    """Class representing EPA Divisions available to the QAPP."""
    
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        """Override str method to display name instead of stringified obj"""
        return self.name


class Qapp(models.Model):
    """Class representing a QAPP. This allows users to easily generate new QAPPs"""
    # Office of Research and Development
    # Center for Environmental Solutions & Emergency Response

    division = models.ForeignKey(Division, blank=False, null=False,
                                 related_name='divisions',
                                 on_delete=models.CASCADE)
    division_branch = models.CharField(blank=False, null=False, max_length=255)
    title = models.CharField(blank=False, null=False, max_length=255)

    # Dynamic number of project leads (project lead, co-leads) one-to-many
    # epa_project_lead_1 = models.CharField(blank=False, null=False, max_length=255)
    # epa_project_lead_2 = models.CharField(blank=False, null=False, max_length=255)

    qa_category = models.CharField(blank=False, null=False, max_length=255) # choice
    intra_extra = models.CharField(blank=False, null=False, max_length=64) # choice
    revision_number = models.CharField(blank=False, null=False, max_length=255)
    date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    prepared_by = models.CharField(blank=False, null=False, max_length=255)
    strap = models.CharField(blank=False, null=False, max_length=255)
    tracking_id = models.CharField(blank=False, null=False, max_length=255)


class QappLead(models.Model):
    """
    Class representing a QAPP project lead. Project has a one-to-many
    relationship with ProjectLead(s)
    """
    
    #project = models.ForeignKey(Qapp,
    #                            blank=False, null=False,
    #                            related_name='projects',
    #                            on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=255)
    project = models.ForeignKey(Qapp, on_delete=models.CASCADE)

    def __str__(self):
        """Override str method to display name instead of stringified obj"""
        return self.name


class QappApproval(models.Model):
    """Class representing the approval page of a QAPP document."""
    project_plan_title = models.CharField(blank=False, null=False,
                                          max_length=255)
    activity_number = models.CharField(blank=False, null=False,
                                       max_length=255)
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    # Dynamic number of signatures, one-to-many:


class QappApprovalSignature(models.Model):
    """Class representing a single signature on a QAPP Approval Page."""
    qapp_approval = models.ForeignKey(QappApproval, blank=False,
                                      on_delete=models.CASCADE)
    intramural = models.BooleanField(blank=False, null=False, default=True)
    name = models.CharField(blank=False, null=False, max_length=255)
    signature = models.CharField(blank=False, null=False, max_length=255)
    date = models.CharField(blank=False, null=False, max_length=255)
    # 6 EPA Project Approvals for Intramural or Extramural:
    # 4 Contractor Approvals for Extramural:

class Attachment(models.Model):
    """Class representing a file attachment to an Existing Data entry."""

    name = models.CharField(blank=False, null=False, max_length=255)
    file = models.FileField(null=True, blank=True, upload_to=get_attachment_storage_path)
    uploaded_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        """Override str method to display name instead of stringified obj"""
        return self.name


class ExistingDataSource(models.Model):
    """Model containing options for the data source dropdown"""

    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        """Override str method to display name instead of stringified obj"""
        return self.name


class ExistingData(models.Model):
    """Class representing an instance of Existing Data Tracking Tool."""

    work = models.CharField(blank=False, null=False, max_length=255)
    email = models.CharField(blank=False, null=False, max_length=255)
    phone = models.CharField(blank=False, null=False, max_length=32)
    search = models.CharField(blank=False, null=False, max_length=255)

    source = models.ForeignKey(ExistingDataSource,
                               blank=False, null=False,
                               related_name='existing_data_sources',
                               on_delete=models.CASCADE)

    source_title = models.CharField(blank=True, null=True, max_length=255)
    keywords = models.CharField(blank=True, null=True, max_length=1024)
    url = models.CharField(blank=True, null=True, max_length=255)

    # Indicates if EPA disclaimer should be included when printing/exporting
    # this data.
    disclaimer_req = models.BooleanField(blank=False)

    # TODO: Consider using this tool to auto-generate a basic citation.
    # https://github.com/thenaterhood/python-autocite
    # Require users to double-check the generated citation before continuing
    citation = models.CharField(blank=False, null=False, max_length=2048)

    date_accessed = models.DateTimeField(blank=False, null=False, default=timezone.now)
    comments = models.CharField(blank=True, null=True, max_length=2048)
    created_by = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    # List of teams with which the Existing Data is shared.
    teams = models.ManyToManyField(Team, through='ExistingDataSharingTeamMap')
    attachments = models.ManyToManyField(Attachment, through='DataAttachmentMap')

    def get_fields(self):
        """Method used in the template to iterate and display all fields."""
        return [(field.name, field.value_to_string(self)) for field in ExistingData._meta.fields]

    def __str__(self):
        """Override str method to display source instead of stringified obj"""
        return self.source_title


class DataAttachmentMap(models.Model):
    """Mapping between Existing Data and uploaded attachments."""

    data = models.ForeignKey(ExistingData, blank=False,
                             related_name='existing_data_attachments',
                             on_delete=models.CASCADE)
    attachment = models.ForeignKey(Attachment, blank=False,
                                   related_name='attachment_existing_data',
                                   on_delete=models.CASCADE)


class ExistingDataSharingTeamMap(models.Model):
    """Mapping between Existing Data and Teams they share."""

    added_date = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    data = models.ForeignKey(ExistingData, blank=False,
                             related_name='existing_data_teams',
                             on_delete=models.CASCADE)
    team = models.ForeignKey(Team, blank=False,
                             related_name='team_existing_data',
                             on_delete=models.CASCADE)
    # Indicates if the team can edit the project.
    can_edit = models.BooleanField(blank=False)

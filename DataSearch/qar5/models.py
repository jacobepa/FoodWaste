# models.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,E1101,W0611,C0411


"""Definition of models."""

from django.db import models
from django.utils import timezone
from constants.utils import get_attachment_storage_path


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
    
    name = models.CharField(blank=False, null=False, max_length=255)
    qapp = models.ForeignKey(Qapp, on_delete=models.CASCADE)

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
    contractor = models.BooleanField(blank=True, null=False, default=False)
    name = models.CharField(blank=True, null=True, max_length=255)
    signature = models.CharField(blank=True, null=True, max_length=255)
    date = models.CharField(blank=True, null=True, max_length=255)
    # 6 EPA Project Approvals for Intramural or Extramural:
    # 4 Contractor Approvals for Extramural:


class SectionA(models.Model):
    """Class representing SectionA (A.3 and later) for a given QAPP"""
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    
    # A3 is readonly, defaults populated in form from constants module.
    a3 = models.CharField(blank=False, null=False, max_length=2047)
    # A4 is user input with an optional chart (a4_chart)
    a4 = models.CharField(blank=False, null=False, max_length=2047)
    a4_chart = models.FileField(null=True, blank=True, upload_to=get_attachment_storage_path)
    # A5 is user input
    a5 = models.CharField(blank=False, null=False, max_length=2047)
    # A6 is user input
    a6 = models.CharField(blank=False, null=False, max_length=2047)
    # A7 is user input
    a7 = models.CharField(blank=False, null=False, max_length=2047)
    # A8 is user input
    a8 = models.CharField(blank=False, null=False, max_length=2047)
    # A9 is mixed defaults and user input, thus we should break it up
    a9 = models.CharField(blank=False, null=False, max_length=2047)
    a9_drive_path = models.CharField(blank=False, null=False, max_length=255)


class SectionB(models.Model):
    """Class representing the entirety of SectionB for a given QAPP"""
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    # B1 Secondary Data will be a dropdown with options from the following: ?
    # analytical methods, animal subjects, cell culture models, existing data,
    # measurements, model application, model development, software development
    #b1_secondary_data = 

    b1_existing_data = models.CharField(blank=False, null=False,
                                        max_length=255)
    b1_data_requirements = models.CharField(blank=False, null=False,
                                            max_length=255)
    b1_databases_maps_literature = models.CharField(blank=False, null=False,
                                                    max_length=255)
    b1_non_quality_constraints = models.CharField(blank=False, null=False,
                                                  max_length=255)

    b2_secondary_data_sources = models.CharField(blank=False, null=False,
                                                 max_length=255)
    b2_process = models.CharField(blank=False, null=False, max_length=255)
    b2_rationale = models.CharField(blank=False, null=False, max_length=255)
    b2_procedures = models.CharField(blank=False, null=False, max_length=255)
    b2_disclaimer = models.CharField(blank=False, null=False, max_length=255)

    b3_process = models.CharField(blank=False, null=False, max_length=255)
    b4_existing_data_tracking = models.CharField(blank=False, null=False,
                                                 max_length=255)


class SectionC(models.Model):
    """Class representing the entirety of SectionC for a given QAPP """
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    # c1 # This TEXT needs to be added automatically
    # c2 # This TEXT needs to be added automatically


class SectionD(models.Model):
    """Class representing the entirety of SectionD for a given QAPP """
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    # d1
    # d2
    # d3

# NOTE: All references are stored and retrievable from
#       EXISTING DATA TRACKING SECTION THIS TOOL
# class References(models.Model):

class Revision(models.Model):
    """
    Class used to track revisions of QAPPs.
    This model has a many-to-one relationship with the Qapp model.
    """
    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    # revision
    # description
    # effective_date
    # initial version
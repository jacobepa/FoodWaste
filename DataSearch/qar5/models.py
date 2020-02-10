# models.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,E1101,W0611,C0411


"""Definition of models."""

from django.db import models
from django.utils import timezone


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

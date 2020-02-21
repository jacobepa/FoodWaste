# models.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,E1101,W0611,C0411


"""Definition of models."""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from constants.utils import get_attachment_storage_path


class Division(models.Model):
    """Class representing EPA Divisions available to the QAPP."""
    
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class SectionBType(models.Model):
    """Class representing Section B Types."""
    
    name = models.CharField(blank=False, null=False, max_length=255)

    def __str__(self):
        """Override str method to display name instead of stringified obj"""
        return self.name


class Qapp(models.Model):
    """Class representing a QAPP. Allows users to easily generate new QAPPs."""

    # Office of Research and Development
    # Center for Environmental Solutions & Emergency Response

    division = models.ForeignKey(Division, blank=False, null=False,
                                 related_name='divisions',
                                 on_delete=models.CASCADE)
    division_branch = models.CharField(
        blank=False, null=False, max_length=255)
    title = models.CharField(blank=False, null=False, max_length=255)
    qa_category = models.CharField(blank=False, null=False, max_length=255)
    intra_extra = models.CharField(blank=False, null=False, max_length=64)
    revision_number = models.CharField(
        blank=False, null=False, max_length=255)
    date = models.DateTimeField(
        blank=False, null=False, default=timezone.now)
    prepared_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    strap = models.CharField(blank=False, null=False, max_length=255)
    tracking_id = models.CharField(blank=False, null=False, max_length=255)

    def save_model(self, request, obj, form, change):
        """
        Overwrite the default save_model method so we can automatically
        set the prepared_by field as current user.
        """
        # Only set prepared_by when it's the first save (create)
        user = request.user
        if not obj.pk:
            obj.prepared_by = request.user
        return super().save_model(request, obj, form, change)

    #def save(user):
    #    """
    #    Overwrite the default save_model method so we can automatically
    #    set the prepared_by field as current user.
    #    """
    #    # Only set prepared_by when it's the first save (create)
    #    if not obj.pk:
    #        obj.prepared_by = request.user
    #    return super().save(commit=True)


class QappLead(models.Model):
    """
    Class representing a QAPP project lead.

    Project has a one-to-many relationship with ProjectLead(s).
    """

    name = models.CharField(blank=False, null=False, max_length=255)
    qapp = models.ForeignKey(Qapp, on_delete=models.CASCADE)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
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


class SectionA(models.Model):
    """Class representing SectionA (A.3 and later) for a given QAPP."""

    qapp = models.OneToOneField(Qapp, on_delete=models.CASCADE,
                                primary_key=True)

    # A3 is readonly, defaults populated in form from constants module.
    a3 = models.CharField(blank=False, null=False, max_length=2047)
    # A4 is user input with an optional chart (a4_chart)
    a4 = models.CharField(blank=False, null=False, max_length=2047)
    a4_chart = models.FileField(null=True, blank=True,
                                upload_to=get_attachment_storage_path)
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
    # Dropdown selection for the SectionB Classificiation
    sectionb_type = models.ForeignKey(SectionBType, blank=True, null=True,
                                      related_name='sectionb_type',
                                      on_delete=models.CASCADE)


class SectionB(models.Model):
    """Class representing the entirety of SectionB for a given QAPP."""

    qapp = models.OneToOneField(Qapp, on_delete=models.CASCADE,
                                primary_key=True)
    # B1 Secondary Data will be a dropdown with options from the following: ?
    # analytical methods, animal subjects, cell culture models, existing data,
    # measurements, model application, model development, software development
    #b1_secondary_data = 
    #b1_1 = 

    b1_2 = models.CharField(blank=False, null=False, max_length=2047)
    b1_3 = models.CharField(blank=False, null=False, max_length=2047)
    b1_4 = models.CharField(blank=False, null=False, max_length=2047)
    b1_5 = models.CharField(blank=False, null=False, max_length=2047)

    b2_1 = models.CharField(blank=False, null=False, max_length=2047)
    b2_2 = models.CharField(blank=False, null=False, max_length=2047)
    b2_3 = models.CharField(blank=False, null=False, max_length=2047)
    b2_4 = models.CharField(blank=False, null=False, max_length=2047)
    b2_5 = models.CharField(blank=False, null=False, max_length=2047)

    b3 = models.CharField(blank=False, null=False, max_length=2047)
    b4 = models.CharField(blank=False, null=False, max_length=2047)


class SectionC(models.Model):
    """Class representing the entirety of SectionC for a given QAPP."""

    qapp = models.OneToOneField(Qapp, on_delete=models.CASCADE,
                                primary_key=True)
    c1 = models.CharField(blank=False, null=False, max_length=2047)
    c2 = models.CharField(blank=False, null=False, max_length=2047)


class SectionD(models.Model):
    """Class representing the entirety of SectionD for a given QAPP."""

    qapp = models.OneToOneField(Qapp, on_delete=models.CASCADE,
                                primary_key=True)
    d1 = models.CharField(blank=False, null=False, max_length=2047)
    d2 = models.CharField(blank=False, null=False, max_length=2047)
    d3 = models.CharField(blank=False, null=False, max_length=2047)


# NOTE: All references are stored and retrievable from
#       EXISTING DATA TRACKING SECTION THIS TOOL
class References(models.Model):
    """
    Class used to store references for the related QAPP.
    """
     
    qapp = models.OneToOneField(Qapp, on_delete=models.CASCADE,
                                primary_key=True)
    references = models.TextField(blank=True, null=True)



class Revision(models.Model):
    """
    Class used to track revisions of QAPPs.

    This model has a many-to-one relationship with the Qapp model.
    This model is referenced in the front-end as Section F.1
    """

    qapp = models.ForeignKey(Qapp, blank=False,
                             on_delete=models.CASCADE)
    revision = models.CharField(blank=False, null=False, max_length=255)
    description = models.CharField(blank=False, null=False, max_length=255)
    effective_date = models.DateTimeField(blank=False, null=False,
                                          default=timezone.now)
    initial_version = models.CharField(
        blank=False, null=False, max_length=255)
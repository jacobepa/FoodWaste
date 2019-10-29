# models.py (constants)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# pylint: disable=line-too-long

"""
Models for the FoodWaste application for constants.

Available functions:
-
"""

SUBJECT_CHOICES = (('General Inquiry', 'General Inquiry'), ('Send Me More Info', 'Send Me More Info'),
                   ('Registration Problem', 'Registration Problem'), ('Log-In Issue', 'Log-In Issue'))
SUBMISSION_CHOICES = (('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'))
SUPPORT_CHOICES = (('', ''), ('foodwaste', 'foodwaste Values'), ('Help', 'Help'),
                   ('Feature', 'Feature Request'), ('Other', 'Other'))

TODO_STATUS_CHOICES = (('', ''), ('Emergency', 'Emergency'), ('Important', 'Important'),
                       ('Back Burner', 'Back Burner'), ('Complete', 'Complete'))

WGK_CHOICES = (('', ''), ('0', 'nwg'), ('1', 'WGK 1'), ('2', 'WGK 2'), ('3', 'WGK 3'))

YN_CHOICES = (('', ''), ('Y', 'Yes'), ('N', 'No'))
ONLY_YN_CHOICES = (('Y', 'Y'),)
YES_OR_NO = ((True, 'Yes'), (False, "No"))

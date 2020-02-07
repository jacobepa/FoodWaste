# models.py (constants)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301

"""
Models for the DataSearch application for constants.

Available functions:
-
"""

SUBJECT_CHOICES = (('General Inquiry', 'General Inquiry'), ('Send Me More Info', 'Send Me More Info'),
                   ('Registration Problem', 'Registration Problem'), ('Log-In Issue', 'Log-In Issue'))
SUBMISSION_CHOICES = (('Submitted', 'Submitted'), ('Under Review', 'Under Review'), ('Accepted', 'Accepted'))
SUPPORT_CHOICES = (('', ''), ('datasearch', 'datasearch Values'), ('Help', 'Help'),
                   ('Feature', 'Feature Request'), ('Other', 'Other'))

TODO_STATUS_CHOICES = (('', ''), ('Emergency', 'Emergency'), ('Important', 'Important'),
                       ('Back Burner', 'Back Burner'), ('Complete', 'Complete'))

WGK_CHOICES = (('', ''), ('0', 'nwg'), ('1', 'WGK 1'), ('2', 'WGK 2'), ('3', 'WGK 3'))

YN_CHOICES = (('', ''), ('Y', 'Yes'), ('N', 'No'))
ONLY_YN_CHOICES = (('Y', 'Y'),)
YES_OR_NO = ((True, 'Yes'), (False, "No"))

DIVISION_CHOICES = ['Groundwater Characterization & Remediation Division',
                    'Homeland Security & Materials Management Division',
                    'Immediate Office', 'Land Remediation & Technology Division',
                    'Technical Support & Coordination Division',
                    'Water Infrastructure Division']

QA_CATEGORY_CHOICES = (('QA Category A', 'QA Category A'),
                       ('QA Category B', 'QA Category B'))

XMURAL_CHOICES = (('Intramural', 'Intramural'), ('Extramural', 'Extramural'))

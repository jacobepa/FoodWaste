# admin.py (teams)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""
Define classes used to generate Django Admin portion of the website.

Available functions:
- Sets Teams
- Sets Team Memberships
"""

from django.contrib import admin
from FoodWaste.models import Attachment, TrackingTool, DataAttachmentMap, \
    SecondaryDataSharingTeamMap

admin.site.register(Attachment)

admin.site.register(TrackingTool)

admin.site.register(DataAttachmentMap)

admin.site.register(SecondaryDataSharingTeamMap)

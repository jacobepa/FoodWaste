# admin.py (DataSearch)
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
from DataSearch.models import Attachment, ExistingData, ExistingDataSource, \
    DataAttachmentMap, ExistingDataSharingTeamMap

admin.site.register(Attachment)

admin.site.register(ExistingData)

admin.site.register(ExistingDataSource)

admin.site.register(DataAttachmentMap)

admin.site.register(ExistingDataSharingTeamMap)

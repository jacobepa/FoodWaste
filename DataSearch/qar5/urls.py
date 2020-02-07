# urls.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# pylint: disable=invalid-name
# We disable the invalid name because urlpatterns is the Django default

"""
URLs related to managing Products

Available functions:
- None yet
"""

from django.conf.urls import url
from qar5.views import ProjectPlanCreate, ProjectPlanDetail, \
    ProjectApprovalCreate, ProjectLeadCreate

urlpatterns = [
    # URLs for CRUD operations.
    # Begin QAPP URLs for creating and printing QAPPs
    url(r'^create/',
        ProjectPlanCreate.as_view(),
        name='qapp_create'),

    url(r'^detail/(?P<pk>\d+)/?$',
        ProjectPlanDetail.as_view(),
        name='qapp_create'),

    url(r'^approval/create/(?P<pk>\d+)/?$',
        ProjectApprovalCreate.as_view(),
        name='qapp_approval'),

    url(r'^project_lead/create/',
        ProjectLeadCreate.as_view(),
        name='get_project_lead_form'),

    #url(r'^project_lead/edit/',
    #    ProjectLeadCreate.as_view(),
    #    name='get_project_lead_form'),
]

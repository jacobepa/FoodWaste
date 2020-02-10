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
from qar5.views import QappCreate, QappDetail, \
    ProjectApprovalCreate, ProjectLeadCreate, ProjectApprovalSignatureCreate, \
    section_b_index, section_c_index, section_d_index, section_e_index, \
    section_f_index

urlpatterns = [
    # URLs for CRUD operations.
    # Begin QAPP URLs for creating and printing QAPPs
    url(r'^create/',
        QappCreate.as_view(),
        name='qapp_create'),

    url(r'^detail/(?P<pk>\d+)/?$',
        QappDetail.as_view(),
        name='qapp_create'),
    
    ############################################
    # Project Approval (and signatures) URLs
    url(r'^approval/create/',
        ProjectApprovalCreate.as_view(),
        name='qapp_approval'),

    # Project Approval Signatures URLs
    url(r'^approval_signature/create/',
        ProjectApprovalSignatureCreate.as_view(),
        name='get_approval_signature_form'),
    
    #url(r'^approval_signature/delete/(?P<pk>\d+)/?$',
    #    get_approval_signature_form.as_view(),
    #    name='get_approval_signature_form'),
    
    #url(r'^approval_signature/detail/(?P<pk>\d+)/?$',
    #    get_approval_signature_form.as_view(),
    #    name='get_approval_signature_form'),

    #url(r'^approval_signature/edit/(?P<pk>\d+)/?$',
    #    get_approval_signature_form.as_view(),
    #    name='get_approval_signature_form'),

    ############################################
    # Project Lead URLs
    url(r'^project_lead/create/',
        ProjectLeadCreate.as_view(),
        name='get_project_lead_form'),
    
    #url(r'^project_lead/delete/(?P<pk>\d+)/?$',
    #    ProjectLeadCreate.as_view(),
    #    name='get_project_lead_form'),
    
    #url(r'^project_lead/detail/(?P<pk>\d+)/?$',
    #    ProjectLeadCreate.as_view(),
    #    name='get_project_lead_form'),

    #url(r'^project_lead/edit/(?P<pk>\d+)/?$',
    #    ProjectLeadCreate.as_view(),
    #    name='get_project_lead_form'),

    ############################################
    # SectionB URLs
    url(r'^SectionB/', section_b_index, name='qapp_sectionb'),
    url(r'^SectionC/', section_c_index, name='qapp_sectionc'),
    url(r'^SectionD/', section_d_index, name='qapp_sectiond'),
    url(r'^SectionE/', section_e_index, name='qapp_sectione'),
    url(r'^SectionF/', section_f_index, name='qapp_sectionf'),
]

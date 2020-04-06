# urls.py (projects)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=invalid-name
# We disable the invalid name because urlpatterns is the Django default

"""
URLs related to managing projects of users.

Available functions:
- REST api for projects
- Project management
"""

from django.conf.urls import url
from projects.views import ProjectCreateView, ProjectDetailView, \
    ProjectEditView, ProjectListView

urlpatterns = [
    url(r'^$', ProjectListView.as_view(), name='projects_list'),
    url(r'^create/?$', ProjectCreateView.as_view(), name='project_create'),
    url(r'^detail/(?P<pk>\d+)/?$',
        ProjectDetailView.as_view(),
        name='project_detail'),
    url(r'^edit/(?P<pk>\d+)/?$',
        ProjectEditView.as_view(),
        name='project_edit'),
]

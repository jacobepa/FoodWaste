# urls.py (scifinder)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for DataSearch."""

from django.conf.urls import url
from scifinder.views import ScifinderDelete, ScifinderIndex, \
    scifinder_download

app_name = 'scifinder'

urlpatterns = [
    url(r'^$', ScifinderIndex.as_view(), name='scifinder_index'),
    # url(r'^download_file/(?P<pk>\d+)/?$',
    #    scifinder_download,
    #    name='scifinder_download'),
    url(r'^delete_file/(?P<pk>\d+)/?$',
        ScifinderDelete.as_view(),
        name='scifinder_delete'),
]

# urls.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for DataSearch."""

from django.conf.urls import url
from flowsa.views import FlowsaDelete, FlowsaIndex, \
    flowsa_download

app_name = 'flowsa'

urlpatterns = [
    url(r'^$', FlowsaIndex.as_view(), name='flowsa_index'),
    #url(r'^download_file/(?P<pk>\d+)/?$',
    #    flowsa_download,
    #    name='flowsa_download'),
    url(r'^delete_file/(?P<pk>\d+)/?$',
        FlowsaDelete.as_view(),
        name='flowsa_delete'),
]

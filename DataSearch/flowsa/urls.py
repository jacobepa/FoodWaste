# urls.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for DataSearch."""

from django.conf.urls import url
from flowsa.views import FlowsaIndex

app_name = 'flowsa'

urlpatterns = [
    url(r'^$', FlowsaIndex.as_view(), name='flowsa_index'),
]

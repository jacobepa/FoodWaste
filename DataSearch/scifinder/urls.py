# urls.py (scifinder)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for DataSearch."""

from django.conf.urls import url
from scifinder.views import ScifinderIndex

app_name = 'scifinder'

urlpatterns = [
    url(r'^$', ScifinderIndex.as_view(), name='scifinder_index'),
]

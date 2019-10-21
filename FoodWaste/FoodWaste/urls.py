# urls.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for FoodWaste."""

from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
from django.urls import include
from FoodWaste.views import home, contact, about, TrackingToolList, TrackingToolCreate


urlpatterns = [
    url(r'^admin/?', admin.site.urls),

    url(r'^$', home, name='home'),
    url(r'^dashboard/$', home, name='dashboard'),
    url(r'^contact/?', contact, name='contact'),
    url(r'^about/?', about, name='about'),
    url(r'^trackingtool/create/?', TrackingToolCreate.as_view(), name='tracking_tool_create'),
    url(r'^trackingtool/?', TrackingToolList.as_view(), name='tracking_tool'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^support/', include('support.urls')),
    url(r'^teams/', include('teams.urls')),
]

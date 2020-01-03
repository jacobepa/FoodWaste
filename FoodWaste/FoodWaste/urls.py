# urls.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for FoodWaste."""

from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from FoodWaste.views import home, contact, about, ExistingDataIndex, \
    ExistingDataList, ExistingDataCreate, ExistingDataDetail, \
    export_pdf, export_excel
from FoodWaste.settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    url(r'^admin', admin.site.urls),

    url(r'^$', home, name='home'),
    url(r'^dashboard', home, name='dashboard'),
    url(r'^contact', contact, name='contact'),
    url(r'^about', about, name='about'),

    # Begin existingdata URLs.
    # URLs for PDF and Excel exports.
    # downloadattachments
    url(r'^existingdata/exportpdf/(?P<pk>\d+)?$',
        export_pdf, name='existing_data_pdf'),
    url(r'^existingdata/exportexcel/(?P<pk>\d+)?$',
        export_excel, name='existing_data_excel'),
    url(r'^existingdata/exportpdf$',
        export_pdf, name='existing_data_pdf'),
    url(r'^existingdata/exportexcel$',
        export_excel, name='existing_data_excel'),

    url(r'^existingdata/create$',
        ExistingDataCreate.as_view(),
        name='existing_data_create'),

    url(r'^existingdata/detail/(?P<pk>\d+)?$',
        ExistingDataDetail.as_view(),
        name='existing_data_detail'),

    # This should be the last existingdata URL.
    url(r'^existingdata/list',
        ExistingDataList.as_view(),
        name='tracking_tool_list'),
    url(r'^existingdata/list/user/(?P<pk>\d+)',
        ExistingDataList.as_view(),
        name='tracking_tool_list'),
    url(r'^existingdata/list/team/(?P<pk>\d+)',
        ExistingDataList.as_view(),
        name='tracking_tool_list'),

    url(r'^existingdata',
        ExistingDataIndex.as_view(),
        name='tracking_tool'),

    # Begin other module import URLs.
    url(r'^accounts/', include('accounts.urls')),
    url(r'^support/', include('support.urls')),
    url(r'^teams/', include('teams.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

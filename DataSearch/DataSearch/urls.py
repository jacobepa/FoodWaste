# urls.py (DataSearch)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of urls for DataSearch."""
import django_saml2_auth.views

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path
from DataSearch.views import home, contact, ExistingDataIndex, \
    ExistingDataList, ExistingDataCreate, ExistingDataDetail, \
    ExistingDataEdit, ExistingDataDelete, web_dev_tools, clean_qapps, \
    attachments_download, attachment_delete

from DataSearch.views_exports import export_pdf_single, export_excel_single, \
    export_doc_single, export
from DataSearch.settings import MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    # ########################################################################
    # Auth SAML
    # ########################################################################
    # SAML2 related URLs. You can change "^saml2_auth/" regex to # any path you
    # want, like "^sso/", "^sso_auth/", "^sso_login/", etc. (required)
    re_path(r'^sso/', include('django_saml2_auth.urls')),

    # The following line will replace default user login with SAML2 (optional)
    # If you want to specific the after-login-redirect-URL,
    # use parameter "?next=/the/path/you/want" with this view.
    re_path(r'^accounts/login/$', django_saml2_auth.views.signin, name='login'),

    # The following line will replace the admin login with SAML2 (optional)
    # If you want to specific the after-login-redirect-URL, use parameter
    # "?next=/the/path/you/want" with this view.
    re_path(r'^admin/login/$', django_saml2_auth.views.signin),
    # ########################################################################
    # END Auth SAML
    # ########################################################################

    re_path(r'^admin', admin.site.urls),

    re_path(r'^$', home, name='home'),
    re_path(r'^dashboard/?$', home, name='dashboard'),
    re_path(r'^contact/?$', contact, name='contact'),

    re_path(r'^dev/?$', web_dev_tools, name='web_dev_tools'),
    re_path(r'^dev/clean_qapps/?$', clean_qapps, name='clean_qapps'),

    # Begin existingdata URLs.
    # URLs for PDF and Excel exports.
    re_path(r'^existingdata/exportpdf/(?P<pk>\d+)/?$',
            export_pdf_single, name='existing_data_pdf'),
    re_path(r'^existingdata/exportpdf/user/(?P<pk>\d+)/?$',
            export, name='existing_data_pdf'),
    re_path(r'^existingdata/exportpdf/team/(?P<pk>\d+)/?$',
            export, name='existing_data_pdf'),

    re_path(r'^existingdata/exportexcel/(?P<pk>\d+)/?$',
            export_excel_single, name='existing_data_excel'),
    re_path(r'^existingdata/exportexcel/user/(?P<pk>\d+)/?$',
            export, name='existing_data_excel'),
    re_path(r'^existingdata/exportexcel/team/(?P<pk>\d+)/?$',
            export, name='existing_data_excel'),

    # URLs for Docx export:
    re_path(r'^existingdata/exportdocx/(?P<pk>\d+)/?$',
            export_doc_single, name='existing_data_docx'),
    re_path(r'^existingdata/exportdocx/user/(?P<pk>\d+)/?$',
            export, name='existing_data_docx'),
    re_path(r'^existingdata/exportdocx/team/(?P<pk>\d+)/?$',
            export, name='existing_data_docx'),
    # I don't think this should get hit?
    re_path(r'^existingdata/exportdocx/?$',
            export, name='existing_data_docx'),


    # Download all attachments for the given datasearch pk
    re_path(r'^existingdata/download_attachments/(?P<pk>\d+)/?$',
            attachments_download, name='attachments_download_all'),
    # Download a single attachment for the given
    # datasearch pk and attachment id
    re_path(r'^existingdata/download_attachment/(?P<pk>\d+)/(?P<id>\d+)/?$',
            attachments_download, name='attachment_download'),

    re_path(r'^existingdata/delete_attachment/(?P<pk>\d+)/(?P<id>\d+)/?$',
            attachment_delete, name='attachment_delete'),


    re_path(r'^existingdata/create/?$',
            ExistingDataCreate.as_view(),
            name='existing_data_create'),

    re_path(r'^existingdata/detail/(?P<pk>\d+)/?$',
            ExistingDataDetail.as_view(),
            name='existing_data_detail'),

    re_path(r'^existingdata/edit/(?P<pk>\d+)/?$',
            ExistingDataEdit.as_view(),
            name='existing_data_edit'),

    re_path(r'^existingdata/delete/(?P<pk>\d+)/?$',
            ExistingDataDelete.as_view(),
            name='existing_data_delete'),

    # This should be the last existingdata URL.
    re_path(r'^existingdata/list/user/(?P<pk>\d+)/?$',
            ExistingDataList.as_view(),
            name='tracking_tool_list'),
    re_path(r'^existingdata/list/team/(?P<pk>\d+)/?$',
            ExistingDataList.as_view(),
            name='tracking_tool_list'),
    re_path(r'^existingdata/list/?$',
            ExistingDataList.as_view(),
            name='tracking_tool_list'),

    re_path(r'^existingdata/?$',
            ExistingDataIndex.as_view(),
            name='tracking_tool'),

    # Begin other module import URLs.
#     re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^flowsa/', include('flowsa.urls', namespace='flowsa')),
    re_path(r'^projects/', include('projects.urls')),
    re_path(r'^qar5/', include('qar5.urls')),
    re_path(r'^scifinder/', include('scifinder.urls', namespace='scifinder')),
    re_path(r'^support/', include('support.urls')),
    re_path(r'^teams/', include('teams.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

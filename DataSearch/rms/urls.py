from django.conf.urls import include, url
from rms.views import *

urlpatterns = [
    #
    #Public URLS
    #
    url(r'^$', index, name='go_to_rms'),
    url(r'^search/$', search_project, name='search_rms_project'),
    url(r'^search/result/$', result_search_project, name='result_search_rms_project'),
    url(r'^show/(?P<project_id>\d+)/$', show_project, name='show_rms_project'),


    #
    # Editor/Admin URLs (Add kwargs after view and before name)
    #
    url(r'^file/upload/(?P<obj_id>\d+)/$', file_upload, kwargs={'perms':'deny'}, name='rms_file_upload'),
    url(r'^project_attachment/delete/(?P<obj_id>\d+)/$', delete_project_attachment, kwargs={'perms':'deny'} ,name='delete_rms_project_attachment'),
]

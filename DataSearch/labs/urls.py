from django.conf.urls import include, url
from labs.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^index/$', index, name='go_to_user_library_labs'),

    url(r'^create/$', create_lab, name='create_lab'),
    url(r'^edit/(?P<obj_id>\d+)/$', edit_lab, name='edit_lab'),
    url(r'^delete/(?P<obj_id>\d+)/$', delete_lab, name='delete_lab'),
    url(r'^list/$', list_labs, name='list_labs'),
    url(r'^search/$', search_lab, name='search_lab'),
    url(r'^search/result/$', result_search_lab, name='result_search_lab'),
    url(r'^show/(?P<obj_id>\d+)/$', show_lab, name='show_lab'),
	url(r'^show/with_assets/(?P<obj_id>\d+)/$', show_lab_with_assets, name='show_lab_with_assets'),
]
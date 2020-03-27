from django.conf.urls import include, url


urlpatterns = patterns('immediate_offices.views',
    url(r'^$', index),
    url(r'^index/$', index, name='go_to_immediate_offices'),
    url(r'^create/$', create_immediate_office, name='create_immediate_office'),
    url(r'^edit/(?P<obj_id>\d+)/$', edit_immediate_office, name='edit_immediate_office'),
    url(r'^delete/(?P<obj_id>\d+)/$', delete_immediate_office, name='delete_immediate_office'),
    url(r'^list/$', list_immediate_offices, name='list_immediate_offices'),
    url(r'^search/$', search_immediate_office, name='search_immediate_office'),
    url(r'^search/result/$', result_search_immediate_office, name='result_search_immediate_office'),
    url(r'^show/(?P<obj_id>\d+)/$', show_immediate_office, name='show_immediate_office'),
)

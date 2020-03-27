from django.conf.urls import include, url


urlpatterns = patterns('offices.views',
    url(r'^$', index),
    url(r'^index/$', index', name='go_to_user_library_offices),

    url(r'^create/$', create_office', name='create_office),
    url(r'^edit/(?P<obj_id>\d+)/$', edit_office', name='edit_office),
    url(r'^delete/(?P<obj_id>\d+)/$', delete_office', name='delete_office),
    url(r'^list/$', list_offices', name='list_offices),
    url(r'^search/$', search_office', name='search_office),
    url(r'^search/result/$', result_search_office', name='result_search_office),
    url(r'^show/(?P<obj_id>\d+)/$', show_office', name='show_office),



)

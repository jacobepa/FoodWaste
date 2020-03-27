from django.conf.urls import include, url


urlpatterns = patterns('divisions.views',
    url(r'^$', index),
    url(r'^index/$', index, name='go_to_user_library_divisions'),
    url(r'^create/$', create_division, name='create_division'),
    url(r'^edit/(?P<obj_id>\d+)/$', edit_division, name='edit_division'),
    url(r'^delete/(?P<obj_id>\d+)/$', delete_division, name='delete_division'),
    url(r'^list/$', list_divisions, name='list_divisions'),
    url(r'^search/$', search_division, name='search_division'),
    url(r'^search/result/$', result_search_division, name='result_search_division'),
    url(r'^show/(?P<obj_id>\d+)/$', show_division, name='show_division'),
    url(r'^list/expand_02/(?P<obj_id>\d+)/$', list_divisions_to_expand_two, name='list_divisions_to_expand_two'),
)

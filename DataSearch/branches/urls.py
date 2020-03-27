from django.conf.urls import include, url


urlpatterns = patterns('branches.views',
    url(r'^$', index),
    url(r'^index/$', index, name='go_to_user_library_branches'),
    url(r'^create/$', create_branch, name='create_branch'),
    url(r'^edit/(?P<obj_id>\d+)/$', edit_branch, name='edit_branch'),
    url(r'^delete/(?P<obj_id>\d+)/$', delete_branch, name='delete_branch'),
    url(r'^list/$', list_branches, name='list_branches'),
    url(r'^search/$', search_branch, name='search_branch'),
    url(r'^search/result/$', result_search_branch, name='result_search_branch'),
    url(r'^show/(?P<obj_id>\d+)/$', show_branch, name='show_branch'),
    url(r'^list/lab/expand/$', list_labs_to_expand, name='list_labs_to_expand'),
    url(r'^list/division/expand/(?P<obj_id>\d+)/$', list_divisions_to_expand, name='list_divisions_to_expand'),
    url(r'^list/expand/(?P<obj_id>\d+)/$', list_branches_to_expand, name='list_branches_to_expand'),
    url(r'^list/expand_02/(?P<obj_id>\d+)/$', list_branches_to_expand_two, name='list_branches_to_expand_two'),
)

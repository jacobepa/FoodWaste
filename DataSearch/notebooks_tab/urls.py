from django.conf.urls import include, url
from .views import *
from notebooks_tab.views import *

urlpatterns = [
    #
    #Public URLS
    #
    url(r'^$', index),
    url(r'^index/$', index, name='go_to_notebooks_tab'),
    url(r'^show/(?P<obj_id>\d+)/$', show_nb_tab, name='show_nb_tab'),
    url(r'^search/$', search_nb_tab, name='search_nb_tab'),
    url(r'^search/result/$', result_search_nb_tab, name='result_search_nb_tab'),
    url(r'^searchsepcustodian/$', search_nb_sepcustodian, name='search_nb_sepcustodian'),
    url(r'^searchsepcustodian/result/$', result_search_nb_sepcustodian, name='result_search_nb_sepcustodian'),
    url(r'^nb_periodic_review/search/$', search_nb_periodic_review, name='search_nb_periodic_review'),
    url(r'^nb_periodic_review/search/result/$', result_search_nb_periodic_review, name='result_search_nb_periodic_review'),
    url(r'^nb_reviews/(?P<nb_id>\d+)/$', nbtab_nb_review, name='nbtab_nb_review'),
    url(r'^user_reviews/(?P<user_id>\d+)/$', nbtab_user_review, name='nbtab_user_review'),
    url(r'^show_nb_review/(?P<review_id>\d+)/$', show_nb_review, name='show_nb_review'),


    #
    # Editor/Admin URLs (Add kwargs after view and before name)
    #
    url(r'^create/$', NotebooksTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_nb_tab_item'),
    url(r'^create/(?P<obj_id>\d+)/$', NotebooksTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_nb_tab_item'),
    url(r'^nb_attachment/update_review_flag/(?P<obj_id>\d+)/$', switch_is_review_file_flag_nb, kwargs={'perms':'deny'}, name='switch_is_review_file_flag_nb'),
    url(r'^nb_attachment/delete/(?P<obj_id>\d+)/$', delete_nbtab_attachment, kwargs={'perms':'deny'}, name='delete_nbtab_attachment'),
    url(r'^review_attachment/delete/(?P<obj_id>\d+)/$', delete_review_attachment, kwargs={'perms':'deny'}, name='delete_review_attachment'),
    url(r'^file/upload/(?P<obj_id>\d+)/$', file_upload_nbtab, kwargs={'perms':'deny'}, name='file_upload_nbtab'),
    url(r'^review_file/upload/(?P<review_id>\d+)/$', file_upload_nbreview, kwargs={'perms':'deny'}, name='file_upload_nbreview'),
    url(r'^edit/(?P<obj_id>\d+)/$', NBTabEditView.as_view(), kwargs={'perms':'deny'}, name='edit_nb_tab_item'),
    url(r'^review_attachment/update_email_flag/(?P<obj_id>\d+)/$', switch_file_email_flag_nb_review, kwargs={'perms':'deny'}, name='switch_file_email_flag_nb_review'),
    url(r'^review_attachment/update_review_flag/(?P<obj_id>\d+)/$', switch_is_review_file_flag_nb_review, kwargs={'perms':'deny'}, name='switch_is_review_file_flag_nb_review'),
    url(r'^org/link/(?P<obj_id>\d+)/$', CreateOrgLink_NB.as_view(), kwargs={'perms':'deny'}, name='link_organization_nb'),
    url(r'^org/delete/(?P<obj_id>\d+)/$', delete_nb_org, kwargs={'perms':'deny'}, name='delete_nb_org'),
    url(r'^nb_annual_review/update_nb_reminder_flag/(?P<obj_id>\d+)/(?P<nb_annual_sql>.*)/(?P<query_show>.*)/$', switch_nb_schedule_review_flag, kwargs={'perms':'deny'}, name='switch_nb_schedule_review_flag'),
    url(r'^set_sched_review/(?P<user_id>\d+)/(?P<nb_id>\d+)/$', nbtab_set_sched_review.as_view(), kwargs={'perms':'deny'}, name='nbtab_set_sched_review'),
    url(r'^set_sched_review/(?P<user_id>\d+)/(?P<nb_id>\d+)/(?P<scrollto>[a-zA-Z0-9]+)/$', nbtab_set_sched_review.as_view(), kwargs={'perms':'deny'}, name='nbtab_set_sched_review'),
    url(r'^create_nb_review/(?P<user_id>\d+)/(?P<nb_id>\d+)/$', nbtab_create_nb_review.as_view(), kwargs={'perms':'deny'}, name='create_nb_review'),
    url(r'^edit_review/(?P<review_id>\d+)/$', nbtab_edit_nb_review.as_view(), kwargs={'perms':'deny'}, name='edit_nb_review'),

]

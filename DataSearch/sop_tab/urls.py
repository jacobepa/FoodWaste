from django.conf.urls import include, url
from .views import *
from .feeds import LatestSOPFeed
from sop_tab.views import *
from django.conf import settings

include_feed = settings.ENABLE_RSS_FEEDS

urlpatterns = [
    #
    # Public URLs
    #
    url(r'^$', index, name='sop_tab_index'),
    url(r'^index/$', index, name='go_to_sop_tab'),
    url(r'^search/$', search_sop_tab, name='search_sop_tab'),
    url(r'^search/result/$', result_search_sop_tab, name='result_search_sop_tab'),
    url(r'^searchsepcontact/$', search_sop_sepcontact, name='search_sop_sepcontact'),
    url(r'^searchsepcontact/result/$', result_search_sop_sepcontact, name='result_search_sop_sepcontact'),
    url(r'^show/(?P<obj_id>\d+)/$', show_sop_tab, name='show_sop_tab'), #obj_id = SOPTab
    url(r'^sop_biennial_review/search/$', search_sop_biennial_review, name='search_sop_biennial_review'),
    url(r'^sop_biennial_review/search/result/$', result_search_sop_biennial_review, name='result_search_sop_biennial_review'),


    #
    # Editor/Admin URLs (Add kwargs after view and before name)
    #

    url(r'^create/$', SOPTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_sop_tab_item'),
    url(r'^create/(?P<obj_id>\d+)/$', SOPTabCreateView.as_view(), kwargs={'perms':'deny'}, name='create_sop_tab_item'), #obj_id = SOPTab
    url(r'^file/upload/(?P<obj_id>\d+)/$', file_upload_soptab, kwargs={'perms':'deny'}, name='file_upload_soptab'), #obj_id = SOPTab
    url(r'^org/link/(?P<obj_id>\d+)/$', CreateOrgLink_SOP.as_view(), kwargs={'perms':'deny'}, name='link_organization_sop'), #obj_id = SOPTab
    url(r'^org/link/$', CreateOrgLink_SOP.as_view(), kwargs={'perms':'deny'}, name='link_organization_sop'),
    url(r'^org/delete/(?P<obj_id>\d+)/$', delete_sop_org, kwargs={'perms':'deny'}, name='delete_sop_org'), #obj_id = SOPTab_Orgs
    url(r'^sop_attachment/update_email_flag/(?P<obj_id>\d+)/$', switch_file_email_flag_sop, kwargs={'perms':'deny'}, name='switch_file_email_flag_sop'), #obj_id = SOPTabAttachment
    url(r'^sop_attachment/update_review_flag/(?P<obj_id>\d+)/$', switch_is_review_file_flag_sop, kwargs={'perms':'deny'}, name='switch_is_review_file_flag_sop'), #obj_id = SOPTabAttachment
    url(r'^sop_attachment/update_latest_sop_flag/(?P<obj_id>\d+)/$', switch_is_latest_SOP_sop, kwargs={'perms':'deny'}, name='switch_is_latest_SOP_sop'), #obj_id = SOPTabAttachment
    url(r'^edit/(?P<obj_id>\d+)/$', SOPTabEditView.as_view(), kwargs={'perms':'deny'}, name='edit_sop_tab_item'), #obj_id = SOPTab
    url(r'^archive/(?P<obj_id>\d+)/$', archive_sop_tab_item, kwargs={'perms':'deny'}, name='archive_sop_tab_item'), #obj_id = SOPTab
    url(r'^new_version/(?P<obj_id>\d+)/$', create_new_sop_version, kwargs={'perms':'deny'}, name='create_new_sop_version'), #obj_id = SOPTab
    url(r'^sop_attachment/delete/(?P<obj_id>\d+)/$', delete_soptab_attachment, kwargs={'perms':'deny'}, name='delete_soptab_attachment'),
    url(r'^sop_biennial_review/update_sop_reminder_flag/(?P<obj_id>\d+)/$', switch_sop_reminder_flag, kwargs={'perms':'deny'}, name='switch_sop_reminder_flag'),#obj_id = SOPTab
]

if include_feed:
    urlpatterns.append(url(r'^feed/$', LatestSOPFeed(), name='sop_feed'))

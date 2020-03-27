from django.conf.urls import include, url
from .views import *
from .feeds import LatestORDQAPPFeed,LatestRapidQAPPFeed
from projects.views import *
from django.conf import settings

include_feed = settings.ENABLE_RSS_FEEDS

urlpatterns = [
    # # # # # # # # # # # # # #
    #
    # Public URLs
    #
    # # # # # # # # # # # # # #
    #Project
    url(r'^$', index, name='go_to_projects'),
    url(r'^search/$', search_project, name='search_project'),
    url(r'^search/result/$', result_search_project, name='result_search_project'),
    url(r'^searchdbissue/$', search_project_dbissue, name='search_project_dbissue'),
    url(r'^searchdbissue/result/$', result_search_project_dbissue, name='result_search_project_dbissue'),
    url(r'^searchseplead/$', search_project_seplead, name='search_project_seplead'),
    url(r'^searchseplead/result/$', result_search_project_seplead, name='result_search_project_seplead'),
    url(r'^show/(?P<project_id>\d+)/$', show_project, name='show_project'),
    url(r'^show_expanded/(?P<project_id>\d+)/$', show_project_expanded, name='show_project_expanded'),
    url(r'^summary/user/(?P<user_id>\d+)/$', ActivitySummaryByUserView.as_view(), name='activity_summary_user'),
    url(r'^tree/$', show_project_tree, name='show_project_tree'),

    #QA Activities
    url(r'^go_to_qlogs/$', go_to_qlogs, name='go_to_qlogs'),
    url(r'^qlog/pdf/(?P<project_log_id>\d+)/$', pdf_qlog, name='pdf_qlog'),
    url(r'^qlog/excel/(?P<project_log_id>\d+)/$', excel_project_logs, name='excel_project_logs'),
    url(r'^qlog/search/$', search_project_log, name='search_project_log'),
    url(r'^qlog/search/result/$', result_search_project_log, name='result_search_project_log'),
    url(r'^qlog/show/(?P<project_log_id>\d+)/$', show_project_log, name='show_project_log'),
    url(r'^qlog/show_expanded/(?P<project_log_id>\d+)/$', show_project_log_expanded, name='show_project_log_expanded'),
    url(r'^qlog/pending_qa_review/$', qa_review_pending, name='qa_review_pending'),

    #Program
    url(r'^program/search/$', search_program, name='search_program'),
    #url(r'^program/search/result/$', result_search_program, name='result_search_program'),
    url(r'^program/show/(?P<obj_id>\d+)/$', show_program, name='show_program'),

    # Extramural Vehicle
    url(r'^vehicle/search/$', search_vehicle, name='search_vehicle'),
    #url(r'^vehicle/search/result/$', result_search_vehicle, name='result_search_vehicle'),
    url(r'^vehicle/show/(?P<obj_id>\d+)/$', show_vehicle, name='show_vehicle'),

    # Annual QAPP Review Tab
    url(r'^go_to_qapp_review/$', go_to_qapp_review, name='go_to_qapp_review'),
    url(r'^qapp_annual_review/search/$', search_qapp_annual_review, name='search_qapp_annual_review'),
    url(r'^qapp_annual_review/search/result/$', result_search_qapp_annual_review, name='result_search_qapp_annual_review'),

    #Reviews
    url(r'^go_to_reviews/$', go_to_reviews, name='go_to_reviews'),
    url(r'^qa_review/show/(?P<project_log_id>\d+)/$', show_review, name='show_review'),
    url(r'^qa_review/search/$', search_qa_review, name='search_qa_review'),
    url(r'^qa_review/search/result/$', result_search_qa_review, name='result_search_qa_review'),

    #Participating Orgs
    url(r'^participating_organization/show/(?P<obj_id>\d+)/$', show_participating_organization, name='show_participating_organization'),
    url(r'^participating_organization/search/$', search_participating_organization, name='search_participating_organization'),
    #url(r'^participating_organization/search/result/$', result_search_participating_organization, name='result_search_participating_organization'),



    # # # # # # # # # # # # # #
    #
    # Editor/Admin URLs (Add kwargs after view and before name)
    #
    # # # # # # # # # # # # # #

    #Project
    url(r'^create/$', ProjectCreateView.as_view(), kwargs={'perms':'deny'}, name='create_project'),
    url(r'^update/(?P<project_id>\d+)/$', ProjectUpdateView.as_view(), kwargs={'perms':'deny'}, name='edit_project'),
    url(r'^file/upload/(?P<obj_id>\d+)/$', file_upload, kwargs={'perms':'deny'}, name='file_upload'),

    #Orgs
    url(r'^org/link/(?P<obj_id>\d+)/$', CreateOrgLink_Project.as_view(), kwargs={'perms':'deny'}, name='link_organization_proj'),
    url(r'^org/delete/(?P<obj_id>\d+)/$', delete_proj_org, kwargs={'perms':'deny'}, name='delete_proj_org'),

    #QA Activity
    url(r'^qlog/file/upload/(?P<obj_id>\d+)/$', file_upload_project_log, kwargs={'perms':'deny'}, name='file_upload_project_log'),
    url(r'^qlog/create/(?P<obj_id>\d+)/(?P<tlp_id>\d+)/$', create_project_log, kwargs={'perms':'deny'}, name='create_project_log'),
    url(r'^qlog/list_for_log/$', create_project_log_no_project, kwargs={'perms':'deny'}, name='create_project_log_no_project'),
    url(r'^qlog/add/(?P<obj_id>\d+)/$', create_project_log_no_tlp, kwargs={'perms':'deny'}, name='create_project_log_no_tlp'),
    url(r'^qlog/add/(?P<obj_id>\d+)/(?P<send_error>\d+)/$', create_project_log_no_tlp, kwargs={'perms':'deny'}, name='create_project_log_no_tlp'),
    url(r'^qlog/edit/(?P<project_log_id>\d+)/$', edit_project_log, kwargs={'perms':'deny'}, name='edit_project_log'),
    url(r'^qlog/clone/(?P<project_log_id>\d+)/$', clone_project_log, kwargs={'perms':'deny'}, name='clone_project_log'),

    #Program
    url(r'^program/create/$', create_program, kwargs={'perms':'deny'}, name='create_program'),
    url(r'^program/edit/(?P<obj_id>\d+)/$', edit_program, kwargs={'perms':'deny'}, name='edit_program'),

    #Extramural Vehicle
    url(r'^vehicle/create/$', create_vehicle, kwargs={'perms':'deny'}, name='create_vehicle'),
    url(r'^vehicle/edit/(?P<obj_id>\d+)/$', edit_vehicle, kwargs={'perms':'deny'}, name='edit_vehicle'),

    #QA Activity Review
    url(r'^qa_review/edit/(?P<project_log_id>\d+)/$', edit_review, kwargs={'perms':'deny'}, name='edit_review'),
    url(r'^qlog_qa_review/file/upload/(?P<obj_id>\d+)/$', file_upload_qa_review, kwargs={'perms':'deny'}, name='file_upload_qa_review'),

    #Participating Orgs
    url(r'^participating_organization/create/$', create_participating_organization, kwargs={'perms':'deny'}, name='create_participating_organization'),
    url(r'^participating_organization/edit/(?P<obj_id>\d+)/$', edit_participating_organization, kwargs={'perms':'deny'}, name='edit_participating_organization'),

    #Project Attachment
    url(r'^project_attachment/delete/(?P<obj_id>\d+)/$', delete_project_attachment, kwargs={'perms':'deny'}, name='delete_project_attachment'),
    url(r'^project_attachment/log_delete/(?P<obj_id>\d+)/$', delete_project_attachment_log, kwargs={'perms':'deny'}, name='delete_project_attachment_log'),
    url(r'^project_attachment/update_qapp_review_flag/(?P<obj_id>\d+)/$', switch_qapp_review_file_flag, kwargs={'perms':'deny'}, name='switch_qapp_review_file_flag'),
    url(r'^project_attachment/update_latest_qapp_flag/(?P<obj_id>\d+)/$', switch_latest_qapp_flag, kwargs={'perms':'deny'}, name='switch_latest_qapp_flag'),

    #QAPP Annual Review
    url(r'^qapp_annual_review/update_qapp_reminder_flag/(?P<obj_id>\d+)/$', switch_qapp_reminder_flag, kwargs={'perms':'deny'}, name='switch_qapp_reminder_flag'),

]

if include_feed:
    urlpatterns.append(url(r'^qapp/rapid_feed/$', LatestRapidQAPPFeed(), name='rapid_qapp_feed'))
    urlpatterns.append(url(r'^qapp/ord_feed/$', LatestORDQAPPFeed(), name='ord_qapp_feed'))

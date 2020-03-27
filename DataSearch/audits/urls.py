from django.conf.urls import include, url
import audits.views

urlpatterns = [
    url(r'^$', audits.views.index),
    url(r'^index/$', audits.views.index, name='go_to_audits'),

    url(r'^audit_type/create/$', audits.views.create_audit_type, name='create_audit_type'),
    url(r'^audit_type/edit/(?P<obj_id>\d+)/$', audits.views.edit_audit_type, name='edit_audit_type'),
    url(r'^audit_type/delete/(?P<obj_id>\d+)/$', audits.views.delete_audit_type, name='delete_audit_type'),
    url(r'^audit_type/list/$', audits.views.list_audit_types, name='list_audit_types'),
    url(r'^audit_type/search/$', audits.views.search_audit_type, name='search_audit_type'),
    url(r'^audit_type/search/result/$', audits.views.result_search_audit_type, name='result_search_audit_type'),
    url(r'^audit_type/show/(?P<obj_id>\d+)/$', audits.views.show_audit_type, name='show_audit_type'),
]
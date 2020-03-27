from django.conf.urls import include, url
from django.contrib import admin

from .views import *

urlpatterns = [
        url(r'^office/edit/(?P<office_id>\d+)/$', OfficeEditView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="office_edit"),
        url(r'^office/delete/(?P<office_id>\d+)/$', OfficeDeleteView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="office_delete"),
        url(r'^office/list/$', OfficeListView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="office_list"),
        url(r'^office/create/$', OfficeCreateView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="office_create"),
        url(r'^office/show/(?P<office_id>\d+)/$', OfficeView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="office_show"),
        url(r'^lab/show/(?P<lab_id>\d+)/$', LabView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="lab_show"),
        url(r'^lab/edit/(?P<lab_id>\d+)/$', LabEditView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="lab_edit"),
        url(r'^lab/delete/(?P<lab_id>\d+)/$', LabDeleteView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="lab_delete"),
        url(r'^lab/create/(?P<office_id>\d+)/$', LabCreateView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="lab_create"),
        url(r'^lab/toggle_active/(?P<lab_id>\d+)/$', LabToggleActiveView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="lab_toggle_active"),
        url(r'^division/show/(?P<division_id>\d+)/$', DivisionView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="division_show"),
        url(r'^division/edit/(?P<division_id>\d+)/$', DivisionEditView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="division_edit"),
        url(r'^division/delete/(?P<division_id>\d+)/$', DivisionDeleteView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="division_delete"),
        url(r'^division/create/(?P<lab_id>\d+)/$', DivisionCreateView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="division_create"),
        url(r'^division/toggle_active/(?P<division_id>\d+)/$', DivisionToggleActiveView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="division_toggle_active"),
        url(r'^branch/show/(?P<branch_id>\d+)/$', BranchView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="branch_show"),
        url(r'^branch/edit/(?P<branch_id>\d+)/$', BranchEditView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="branch_edit"),
        url(r'^branch/delete/(?P<branch_id>\d+)/$', BranchDeleteView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="branch_delete"),
        url(r'^branch/create/(?P<division_id>\d+)/$', BranchCreateView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="branch_create"),
        url(r'^branch/toggle_active/(?P<branch_id>\d+)/$', BranchToggleActiveView.as_view(), kwargs={'perms':'deny','level':'admin'}, name="branch_toggle_active")
]

# urls.py (accounts)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=invalid-name
# We disable the invalid name because urlpatterns is the Django default.
# py-lint: disable=C0301

"""
Module related to urls for user accounts.

Available functions:
- Login
- View/edit profile
- New user registration
- Password Management
- Username management
"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import ProfileView, ChangePasswordView, \
    UserRegistrationView, AccountsAdminView, UserSearchView, \
    UserUpdateView, PasswordResetRequestView, PasswordResetConfirmView, \
    UsernameReminderRequestView

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^password/$', ChangePasswordView.as_view(), name='password_change'),
    url(r'^register/$', UserRegistrationView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='registration/logout.html'), name="logout"),
    url(r'^manage/$', AccountsAdminView.as_view(), name="accounts_manage"),
    url(r'^manage/user/$', UserSearchView.as_view(), name='user_select'),
    url(r'^manage/user/(?P<user_id>\d+)/$', UserUpdateView.as_view(), name='user_edit'),

    # password management
    url(r'^password/reset/$', PasswordResetRequestView.as_view(), name="password_reset"),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(), name='reset_password_confirm_no_token'),

    url(r'^username/$', UsernameReminderRequestView.as_view(), name="username_reminder"),
]

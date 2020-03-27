from django.conf.urls import url
from .views import *

from django.contrib.auth.views import(
    LoginView,
    LogoutView
)
import accounts.views

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
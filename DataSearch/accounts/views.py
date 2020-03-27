from django.shortcuts import render
#
# Views for login/logout and user management
#
#


import urllib.parse
from django.db.models import Q
from organization.models import *
from django.contrib.sessions.models import Session
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import FormView, TemplateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
import organization.query_utils as oq

from django.core.validators import validate_email
from django.http import HttpResponseRedirect, QueryDict
from django.forms import widgets, ModelForm, ValidationError
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes

# auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from constants.perms import apply_perms
from django.utils import timezone


class UsernameReminderRequestView(FormView):
    """
    View for forgotten username
    """
    form_class = UsernameReminderRequestForm
    messages = None
    template_name = "registration/username_reminder.html"
    template_done = "registration/username_reminder_done.html"
    # email and subject line templates
    subject_template_name='registration/username_reminder_subject.txt'
    email_template_name='registration/username_reminder_email.html'

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @apply_perms
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data["email"]

            if self.validate_email_address(data) is True:                 #uses the method written above
                # find the users associated with this email that are active
                associated_users= User.objects.filter(Q(email__iexact=data)&Q(is_active__exact=True))
                #associated_users= User.objects.filter(Q(email_iexact=data)|Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': settings.SITE_NAME,
                            'app_name': settings.APP_NAME,
                            'user': user,
                            'protocol': 'http'
                        }
                        subject = loader.render_to_string(self.subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(self.email_template_name, c)
                        send_mail(subject, email, settings.DEFAULT_QATRACK_EMAIL , [user.email], fail_silently=False)
                    # render the done page
                    return render(request, self.template_done, locals())


                result = self.form_invalid(form)
                messages.error(request, 'No active user is associated with this email address')
                return result
            else:
                # email is not valid
                result = self.form_invalid(form)
                messages.error(request, 'Please enter a valid email address.')
                return result

        except Exception as e:
            print(e)
        return self.form_invalid(form)


class PasswordResetRequestView(FormView):
    """
    View for starting the password reset process.
    This view renders the form to enter a username or email address.
    Upon successful entry of a user/email, an email is sent with password reset instructions
    and a confirmation message displayed.
    """
    form_class = PasswordResetRequestForm
    template_name = "registration/password_reset.html"
    template_email_sent = "registration/password_reset_email_sent.html"
    # email and subject line templates
    subject_template_name='registration/password_reset_subject.txt'
    email_template_name='registration/password_reset_email.html'

    @staticmethod
    def validate_email_address(email):

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @apply_perms
    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        try:
            # make sure the user entered something into the form
            if form.is_valid():
                data = form.cleaned_data["email_or_username"]
            else:
                result = self.form_invalid(form)
                messages.error(request, 'Please enter a valid email address or username')
                return result

            # determine if the email address or username matches an account AND the account is active.
            # We don't want to confuse people by letting them reset pw if they don't have an active
            # account because then they will reset their pw but receive an error when they try to log in.
            if self.validate_email_address(data) is True:
                # user entered an email address
                associated_users= User.objects.filter((Q(email__iexact=data)|Q(username__iexact=data))&Q(is_active__exact=True))
                if associated_users.exists() is False:
                    result = self.form_invalid(form)
                    messages.error(request, 'No active user is associated with this email address')
                    return result
            else:
                associated_users= User.objects.filter(Q(username__iexact=data)&Q(is_active__exact=True))
                if associated_users.exists() is False:
                    result = self.form_invalid(form)
                    messages.error(request, 'This username does not exist or is inactive in the system.')
                    return result

            # send an email to the user with a password reset token
            for user in associated_users:
                c = {
                    'email': user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': settings.SITE_NAME,
                    'app_name': settings.APP_NAME,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }

                subject = loader.render_to_string(self.subject_template_name, c)
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(self.email_template_name, c)
                send_mail(subject, email, settings.DEFAULT_QATRACK_EMAIL , [user.email], fail_silently=False)

            # render the done page
            print("RENDER THE DONE PAGE")
            return render(request, self.template_email_sent, locals())

        except Exception as e:
            print(e)
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    """
    This view handles the actual password reset for a user that has forgotten their
    password.
    The view first checks the hash in a password reset link and then
    presents a form to enter a new password

    """
    template_confirm = "registration/password_reset_confirm.html"
    template_no_token = "registration/password_reset_confirm_no_token.html"
    template_done = "registration/password_reset_done.html"
    form_class = SetPasswordForm

    @apply_perms
    def get(self, request, uidb64=None, token=None, **kwargs):
        """
        Responds to link from password reset email
        """
        form = self.form_class(None)
        if uidb64 is None or token is None:
            return render(request, self.template_no_token, locals())
        else:
            UserModel = get_user_model()
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = UserModel._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None
            if user is None or default_token_generator.check_token(user, token) is False:
                return render(request, self.template_no_token, locals())

        return render(request, self.template_confirm, locals())

    @apply_perms
    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        form = self.form_class(request.POST)

        UserModel = get_user_model()
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()

                return render(request, self.template_done, locals())
            else:
                print('Form Not Valid')
                messages.error(request, 'Password reset was unsuccessful. Please try again')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)


class ProfileView(FormView):
    """
    View of the user account information
    """
    form_class = ProfileUpdateForm
    template_profile = "main/profile.html"

    def _setup_organization_select(self, user):
        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

        # formatting for the organization selector
        office_required = True
        lab_required = True
        division_required = True
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        return (office_list, lab_list, division_list, branch_list,
                office_required, lab_required, division_required, label_class, input_container_class,)

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, **kwargs):
        """
        Display the user profile
        """
        user = request.user
        (office_list, lab_list, division_list, branch_list,
         office_required, lab_required, division_required,
         label_class, input_container_class,) = self._setup_organization_select(user)
        selected_office = user.userprofile.office
        selected_lab = user.userprofile.lab
        selected_division = user.userprofile.division
        selected_branch = user.userprofile.branch
        show_inactive_orgs = 'on'

        form = self.form_class(instance=user, is_admin_view=False, user=request.user)

        print("USER IS ACTIVE",user.is_active)
        return render(request, self.template_profile, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        """
        Save the changes to the user form
        """
        user = request.user
        (office_list, lab_list, division_list, branch_list,
         office_required, lab_required, division_required,
         label_class, input_container_class,) = self._setup_organization_select(user)
#        selected_office = user.userprofile.office
#        selected_lab = user.userprofile.lab
#        selected_division = user.userprofile.division
#        selected_branch = user.userprofile.branch

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        selected_office = Office.objects.get(id=office_id) if oq._valid_org_id(office_id) else None
        selected_lab = Lab.objects.get(id=lab_id) if oq._valid_org_id(lab_id) else None
        selected_division = Division.objects.get(id=division_id) if oq._valid_org_id(division_id) else None
        selected_branch = Branch.objects.get(id=branch_id) if oq._valid_org_id(branch_id) else None

        if not kwargs["is_admin"]:
            # disabled fields are not passed with the form, so add a few things to the POST
            updated_post = request.POST.copy()
            if user.userprofile.office is not None:
                updated_post['office'] = user.userprofile.office.id
            if user.userprofile.lab is not None:
                updated_post['lab'] = user.userprofile.lab.id
#            if user.userprofile.division is not None:
#                updated_post['division'] = user.userprofile.division.id
#            if user.userprofile.branch is not None:
#                updated_post['branch'] = user.userprofile.branch.id
#            updated_post['is_superuser'] = user.is_superuser
#            updated_post['user_type'] = user.userprofile.user_type
            updated_post['is_staff'] = user.is_staff
            updated_post['permissions'] = user.userprofile.permissions
#            updated_post['is_reviewer'] = user.userprofile.is_reviewer
            # updated_post['is_technical_lead'] = user.userprofile.is_technical_lead
#            updated_post['can_edit'] = user.userprofile.can_edit
#            updated_post['can_create_users'] = user.userprofile.can_create_users

            form = self.form_class(updated_post, instance=user, is_admin_view=False, user=request.user)
        else:
            form = self.form_class(request.POST, instance=user, is_admin_view=False, user=request.user)

        if form.is_valid():
            # save the user information and get a pointer to the User object
            user = form.save()
            # if the password information was changed, make sure the current password is
            # correct
            success = True
        else:
            form = self.form_class(instance=user, is_admin_view=False, user=request.user)

        return render(request, self.template_profile, locals())


class ChangePasswordView(FormView):
    """
    View of the user account information
    """
    form_class = ChangePasswordForm
    template_profile = "main/password_change.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, **kwargs):
        """
        Display the user profile
        """
        form = ChangePasswordForm(instance=request.user)
        return render(request, self.template_profile, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        """
        Save the changes to the user form
        """
        user = request.user
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            # save the user information and get a pointer to the User object
            user = form.save()
            # if the password information was changed, make sure the current password is
            # correct
            success = True

        return render(request, self.template_profile, locals())


class UserRegistrationView(FormView):
    """
    View for registering a new user.  Restricted to super users
    """
    form_class = ProfileCreationForm
    template_register = "registration/register.html"

    def _setup_organization_select(self, user):
        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

        # formatting for the organization selector
        office_required = True
        lab_required = True
        division_required = True
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        return (office_list, lab_list, division_list, branch_list,
                office_required, lab_required, division_required, label_class, input_container_class)

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Render the user registration template
        """

        user = request.user
        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(user)
        selected_office = user.userprofile.office

#        if not request.user.is_superuser:
#            # only super users can register new users
#            return HttpResponseRedirect(reverse('home'))

        form = self.form_class(user=request.user)
        return render(request, self.template_register, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        """
        Process the user's registration request
        """
#        if not request.user.is_superuser:
#            # only super users can register new users
#            return HttpResponseRedirect(reverse('home'))

        postdata = request.POST.copy()
        postdata["date_joined"] = timezone.now()
        form = self.form_class(postdata, user=request.user)

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        if form.is_valid():
            # save the user information and get a pointer to the User object
            user = form.save()
            success = True

            return HttpResponseRedirect('/accounts/manage/user/' + str(user.id))
        else:
            user = request.user
            (office_list, lab_list, division_list, branch_list, office_required,
             lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(
                user)

            selected_office = Office.objects.get(id=office_id) if oq._valid_org_id(office_id) else None
            selected_lab = Lab.objects.get(id=lab_id) if oq._valid_org_id(lab_id) else None
            selected_division = Division.objects.get(id=division_id) if oq._valid_org_id(division_id) else None
            selected_branch = Branch.objects.get(id=branch_id) if oq._valid_org_id(branch_id) else None

            return render(request, self.template_register, locals())


class AccountsAdminView(TemplateView):
    """
    Main entry point for account management page
    """
    template_register = "main/manage_accounts.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Render the user registration template
        """
#        if not request.user.is_superuser:
#            # only super users can access the admin views
#            return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_register, locals())


class UserSearchView(TemplateView):
    template_register = "main/manage_search_users.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        user_perms = request.user.userprofile.permissions
        user_lab = request.user.userprofile.lab_id
        return render(request, self.template_register, locals())


class UserUpdateView(TemplateView):
    """
    """
    form_class = ProfileUpdateForm
    template_profile = "main/manage_edit_user.html"

    def _setup_organization_select(self, user):
        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

        # formatting for the organization selector
        office_required = True
        lab_required = True
        division_required = True
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        return (office_list, lab_list, division_list, branch_list,
                office_required, lab_required, division_required, label_class, input_container_class)

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Display the user profile
        """
        id = self.kwargs['user_id']
#        if id is None or (request.user.id != id and not request.user.is_superuser):
#            # only super users can edit someone else's profile
#            return HttpResponseRedirect(reverse('home'))

        edit_user = User.objects.get(id=id)

        # Fixed this to get lists according to the request user, not the edit_user.
        # Request user should be an admin, they be able to change what org a user belongs to.
        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(request.user)

        selected_office = edit_user.userprofile.office
        selected_lab = edit_user.userprofile.lab
        selected_division = edit_user.userprofile.division
        selected_branch = edit_user.userprofile.branch

        # Check "Show Inactive organization units" only if current org is inactive.
        if selected_lab and selected_lab.is_active == False:
            show_inactive_orgs = 'on'
        elif selected_division and selected_division.is_active == False:
            show_inactive_orgs = 'on'
        elif selected_branch and selected_branch.is_active == False:
            show_inactive_orgs = 'on'

        form = self.form_class(instance=edit_user, is_admin_view=True, user=request.user)
        return render(request, self.template_profile, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        """
        Save the changes to the user form
        """
        id = self.kwargs['user_id']
#        if id is None or (request.user.id != id and not request.user.is_superuser):
#            # only super users can edit someone else's profile
#            return HttpResponseRedirect(reverse('home'))

        edit_user = User.objects.get(id=id)
        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(
            edit_user)
#        selected_office = edit_user.userprofile.office
#        selected_lab = edit_user.userprofile.lab
#        selected_division = edit_user.userprofile.division
#        selected_branch = edit_user.userprofile.branch

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)


        selected_office = Office.objects.get(id=office_id) if oq._valid_org_id(office_id) else None
        selected_lab = Lab.objects.get(id=lab_id) if oq._valid_org_id(lab_id) else None
        selected_division = Division.objects.get(id=division_id) if oq._valid_org_id(division_id) else None
        selected_branch = Branch.objects.get(id=branch_id) if oq._valid_org_id(branch_id) else None

        form = self.form_class(request.POST, instance=edit_user, is_admin_view=True, user=request.user)

        if form.is_valid():
            print("HERE")
            # save the user information and get a pointer to the User object
            edit_user = form.save()
            success = True

        #return render(request, self.template_profile, locals())
        url = '/accounts/manage/user/%s/' % str(id)
        return HttpResponseRedirect(url)

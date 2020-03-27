#
#
# Forms related to login/logout and user management
#
#

from django import forms
from django.forms import widgets, ModelForm, ValidationError
from django.forms.widgets import SelectDateWidget
from django.forms.models import inlineformset_factory
from django.utils import timezone

from constants.models import *
from accounts.models import *

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import check_password, make_password
import datetime

class UsernameReminderRequestForm(forms.Form):
    """
    Form to enter email when the user has forgotten their username
    """
    email = forms.CharField(label=("Enter your email address"), max_length=254, required=True,
                            widget=forms.TextInput(attrs={'class':'form-control'}))

class PasswordResetRequestForm(forms.Form):
    """
    Form to enter username or email when a password reset is required
    """
    email_or_username = forms.CharField(label=("Enter your email address or username"), max_length=254,
                                        required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                help_text = _("30 characters or fewer. Letters, digits and @ only."),
                                error_messages = {'invalid': _("This value may contain only letters, numbers and @  characters.")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
                                help_text = _("Enter the same password as above, for verification."))
    email = forms.CharField(label=_("Email Address"), widget=forms.TextInput())
    first_name = forms.CharField(label=_("First Name"), widget=forms.TextInput())
    last_name = forms.CharField(label=_("Last Name"), widget=forms.TextInput())
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
                                help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
                                error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class ProfileCreationForm(forms.ModelForm):
    """
    Form to create a new user
    """
    required_css_class = 'required'

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(attrs={'class':'form-control'}))

    first_name = forms.CharField(label=_("First name"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label=_("Last name"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label=_("Email address"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    ## user profile fields
    email_address_epa = forms.CharField(label="EPA Email Address", widget=forms.TextInput(), required=False)
    email_address_other = forms.CharField(label="Alternate Email Address", widget=forms.TextInput(), required=False)

    # these are only here for validation - use the organization_select.html widget
    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                 widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    branch = forms.ModelChoiceField(label=_("Branch"), queryset=Branch.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=False)


    # security / access fields

#    is_staff = forms.TypedChoiceField(label=_("Can log in to Django Admin Tool"),
#                                      widget=forms.Select(attrs={'class':'form-control'}),
#                                      choices=BOOLEAN_YES_NO, required=False)
    is_active = forms.TypedChoiceField(label=_("Can log in to QA Track"),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       choices=BOOLEAN_YES_NO, required=False)
#
#    # Changed initial value from SUPER USER to SINGLE LAB
#    # I think SUPER USER was default only because it was the first choice in dropdown.
#    user_type = forms.TypedChoiceField(label=_("User type"),
#                                       widget=forms.Select(attrs={'class':'form-control'}),
#                                       initial='DIVISION', # Changed initial value from SUPER USER to DIVISION USER
#                                       choices=USER_TYPE_CHOICES, required=False)

    permissions = forms.TypedChoiceField(label=_("User permissions"),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       initial='READER',
                                       choices=PERMISSION_CHOICES, required=True)

    # is_reviewer = forms.TypedChoiceField(label=_("Is reviewer"),
    #                                      widget=forms.Select(attrs={'class':'form-control'}),
    #                                      choices=YN_CHOICES, required=True)
    # is_technical_lead = forms.TypedChoiceField(label=_("Is technical lead"),
    #                                            widget=forms.Select(attrs={'class':'form-control'}),
    #                                            choices=YN_CHOICES, required=True)
#    can_edit = forms.TypedChoiceField(label=_("Can edit"),
#                                      widget=forms.Select(attrs={'class': 'form-control'}),
#                                      choices=YN_CHOICES, required=False)
#    is_superuser = forms.TypedChoiceField(label=_("Can access Manage tab"),
#                                          widget=forms.Select(attrs={'class': 'form-control'}),
#                                          choices=BOOLEAN_YES_NO, required=False)
#    can_create_users = forms.TypedChoiceField(label=_("Can create users"),
#                                              widget=forms.Select(attrs={'class':'form-control'}),
#                                              choices=YN_CHOICES, required=False)

    # password
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text = _("Enter the same password as above, for verification."))


    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("The username you selected is already in use.  Please try a different username."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The passwords you entered did not match.  Please try again."))
        return password2


    def save(self, commit=True):
        user = User.objects.create_user(self.clean_username(),
                                        self.cleaned_data["email"],
                                        self.cleaned_data["password1"])
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
#        user.is_superuser = (self.cleaned_data["is_superuser"] == 'True')
        user.is_staff = (self.cleaned_data["permissions"] == 'ADMIN')
        user.is_active = (self.cleaned_data["is_active"] == 'True')
        user.save()

        user.userprofile = UserProfile.objects.create(user=user)
        user.userprofile.office = self.cleaned_data["office"]
        user.userprofile.lab = self.cleaned_data["lab"]
        user.userprofile.division = self.cleaned_data["division"]
        user.userprofile.branch = self.cleaned_data["branch"]
        user.userprofile.email_address_epa = self.cleaned_data["email_address_epa"]
        user.userprofile.email_address_other = self.cleaned_data["email_address_other"]
        user.userprofile.permissions = self.cleaned_data["permissions"]
#        user.userprofile.user_type = self.cleaned_data["user_type"]
        # user.userprofile.is_reviewer = self.cleaned_data["is_reviewer"]
        # user.userprofile.is_technical_lead = self.cleaned_data["is_technical_lead"]
#        user.userprofile.can_edit = self.cleaned_data["can_edit"]
#        user.userprofile.can_create_users = self.cleaned_data["can_create_users"]

        user.userprofile.save()

        return user

    def __init__(self, *args, **kw):
        self.user = kw.pop('user') if 'user' in kw else User
        super(ProfileCreationForm, self).__init__(*args, **kw)
        if self.user.userprofile.permissions == 'EDITOR':
            self.fields['permissions'].choices = EDITOR_PERMISSION_CHOICES

    class Meta:
        model = User
        fields = ('username', 'last_login', 'date_joined', 'first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    """
    Form to update
    """
    required_css_class = 'required'

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput(attrs={'class':'form-control','readonly': 'readonly'}))
    last_login = forms.DateTimeField(label=_("Last Login"), required=False,
                                     widget=forms.DateInput(
                                         format='%Y-%m-%d %I:%M:%S %Z',
                                         attrs={'class':'form-control','readonly': 'readonly'}))
    first_name = forms.CharField(label=_("First name"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label=_("Last name"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label=_("Email address"), required=True, widget=forms.TextInput(attrs={'class':'form-control'}))

    date_joined = forms.DateTimeField(label=_("Account created"),
                                      widget=forms.DateInput(
                                          format='%Y-%m-%d %I:%M:%S %Z',
                                          attrs={'class':'form-control','readonly': 'readonly'}))

    ## user profile fields
    email_address_epa = forms.CharField(label="EPA Email Address", widget=forms.TextInput(), required=False)
    email_address_other = forms.CharField(label="Alternate Email Address", widget=forms.TextInput(), required=False)

    # these are only here for validation - use the organization_select.html widget
    branch = forms.ModelChoiceField(label=_("Branch"), queryset=Branch.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  required=False)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  required=False)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  required=True)
    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                  widget=forms.Select(attrs={'class':'form-control'}),
                                  required=True)


    # security / access fields

#    is_staff = forms.TypedChoiceField(label=_("Can log in to Django Admin Tool"),
#                                      widget=forms.Select(attrs={'class':'form-control'}),
#                                      choices=BOOLEAN_YES_NO, required=False)
#
    is_active = forms.TypedChoiceField(label=_("Can log in to QA Track"),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       choices=BOOLEAN_YES_NO, required=False)
#
#    user_type = forms.TypedChoiceField(label=_("User type"),
#                                       widget=forms.Select(attrs={'class':'form-control'}),
#                                       choices=USER_TYPE_CHOICES, required=False)

    permissions = forms.TypedChoiceField(label=_("User permissions"),
                                       widget=forms.Select(attrs={'class':'form-control'}),
                                       choices=PERMISSION_CHOICES, required=True)


    # is_reviewer = forms.TypedChoiceField(label=_("Is reviewer"),
    #                                      widget=forms.Select(attrs={'class':'form-control'}),
    #                                      choices=YN_CHOICES, required=True)
    # is_technical_lead = forms.TypedChoiceField(label=_("Is technical lead"),
    #                                            widget=forms.Select(attrs={'class':'form-control'}),
    #                                            choices=YN_CHOICES, required=True)
#    can_edit = forms.TypedChoiceField(label=_("Can edit"),
#                                      widget=forms.Select(attrs={'class': 'form-control'}),
#                                      choices=YN_CHOICES, required=False)
#    is_superuser = forms.TypedChoiceField(label=_("Can access Manage tab"),
#                                          widget=forms.Select(attrs={'class': 'form-control'}),
#                                          choices=BOOLEAN_YES_NO, required=False)
#    can_create_users = forms.TypedChoiceField(label=_("Can create users"),
#                                              widget=forms.Select(attrs={'class':'form-control'}),
#                                              choices=YN_CHOICES, required=False)

    # password
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text = _("Enter the same password as above, for verification."))


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The passwords you entered did not match.  Please try again."))
        return password2

    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def __init__(self, *args, **kw):
        """
        Set the fields from the user profile, since these don't get filled in from the User model
        """
        self.is_admin_view = kw.pop('is_admin_view') if 'is_admin_view' in kw else False
        self.user = kw.pop('user') if 'user' in kw else User
        super(ProfileUpdateForm, self).__init__(*args, **kw)
        print(self.user)
        profile = self.instance.userprofile
        self.fields['office'].initial = profile.office
        self.fields['lab'].initial = profile.lab
        self.fields['division'].initial = profile.division
        self.fields['branch'].initial = profile.branch
        self.fields['email_address_epa'].initial = profile.email_address_epa
        self.fields['email_address_other'].initial = profile.email_address_other
        self.fields['permissions'].initial = profile.permissions
        self.fields['is_active'].initial = self.instance.is_active
#        self.fields['user_type'].initial = profile.user_type
        #self.fields['is_reviewer'].initial = profile.is_reviewer
        #self.fields['is_technical_lead'].initial = profile.is_technical_lead
#        self.fields['can_edit'].initial = profile.can_edit
#        self.fields['can_create_users'].initial = profile.can_create_users

        if self.user.userprofile.permissions == 'EDITOR':
            self.fields['permissions'].choices = EDITOR_PERMISSION_CHOICES
        if self.user.userprofile.permissions == 'READER':
            self.fields['permissions'].choices = READER_PERMISSION_CHOICES
            self.fields['is_active'].widget.attrs['disabled'] = True

        #if not self.is_admin_view:
#            self.fields['is_superuser'].widget.attrs['disabled'] = True
#            self.fields['is_active'].widget.attrs['disabled'] = True
#            self.fields['is_staff'].widget.attrs['disabled'] = True
#            self.fields['user_type'].widget.attrs['disabled'] = True
#            #self.fields['is_reviewer'].widget.attrs['disabled'] = True
#            #self.fields['is_technical_lead'].widget.attrs['disabled'] = True
#            self.fields['can_edit'].widget.attrs['disabled'] = True
#            self.fields['can_create_users'].widget.attrs['disabled'] = True
        #else:
#            if not self.user.is_superuser:
#                self.fields['is_superuser'].widget.attrs['disabled'] = True
#                self.fields['is_active'].widget.attrs['disabled'] = True
#                self.fields['is_staff'].widget.attrs['disabled'] = True
#                self.fields['user_type'].widget.attrs['disabled'] = True
#                #self.fields['is_reviewer'].widget.attrs['disabled'] = True
#                #self.fields['is_technical_lead'].widget.attrs['disabled'] = True
#                self.fields['can_edit'].widget.attrs['disabled'] = True
#                self.fields['can_create_users'].widget.attrs['disabled'] = True

        self.fields['password1'].required = False
        self.fields['password2'].required = False


    def save(self, commit=True):
        print("SAVING")
        user = self.instance
        if self.is_admin_view:
            new_password = self.cleaned_data["password2"]
            if len(new_password) > 0:
                user.password = make_password(new_password)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
#        user.is_superuser = (self.cleaned_data["is_superuser"] == "True")
        user.is_staff = (self.cleaned_data["permissions"] == "ADMIN")

        print("IS ACTIVE",self.cleaned_data["is_active"], type(self.cleaned_data["is_active"]), self.instance.is_active)
        if self.cleaned_data["is_active"] != "":
            user.is_active = (self.cleaned_data["is_active"] == "True")
        else:
            user.is_active = self.instance.is_active

        user.userprofile.office = self.cleaned_data["office"]
        user.userprofile.lab = self.cleaned_data["lab"]
        user.userprofile.division = self.cleaned_data["division"]
        user.userprofile.branch = self.cleaned_data["branch"]
        user.userprofile.email_address_epa = self.cleaned_data["email_address_epa"]
        user.userprofile.email_address_other = self.cleaned_data["email_address_other"]
        user.userprofile.permissions = self.cleaned_data["permissions"]
#        user.userprofile.user_type = self.cleaned_data["user_type"]
        #user.userprofile.is_reviewer = self.cleaned_data["is_reviewer"]
        #user.userprofile.is_technical_lead = self.cleaned_data["is_technical_lead"]
#        user.userprofile.can_edit = self.cleaned_data["can_edit"]
#        user.userprofile.can_create_users = self.cleaned_data["can_create_users"]

        # save the user profile and user objects
        user.userprofile.save()
        user.save()

        if self.user.userprofile.permissions == 'EDITOR':
            self.fields['permissions'].choices = EDITOR_PERMISSION_CHOICES
        if self.user.userprofile.permissions == 'READER':
            self.fields['permissions'].choices = READER_PERMISSION_CHOICES

        return user

    class Meta:
        model = User
        fields = ('username', 'last_login', 'date_joined', 'first_name', 'last_name', 'email')




class ChangePasswordForm(forms.ModelForm):
    """
    Form for updating the current user's password
    """
    required_css_class = 'required'

    current_password = forms.CharField(label=_("Current Password"),
                                       widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                       required=True)
    password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                required=True)
    password2 = forms.CharField(label=_("New Password confirmation"),
                                widget=forms.PasswordInput(attrs={'class':'form-control'}),
                                help_text = _("Enter the same password as above, for verification."),
                                required=True)

    def clean_current_password(self):
        """
        Make sure the current password is correct
        """
        user = self.instance
        if len(self.cleaned_data["current_password"]) > 0 and \
                not check_password(self.cleaned_data["current_password"], user.password):
            raise forms.ValidationError(_("The current password was incorrect. Please try again."))
        return self.cleaned_data["current_password"]

    def clean_password2(self):
        """
        Verify that the new passwords match
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The passwords you entered did not match.  Please try again."))
        return password2

    def save(self, commit=True):
        user = self.instance
        # reset the password
        new_password = self.cleaned_data["password2"]
        if len(new_password) > 0:
            user.password = make_password(new_password)
        user.save()
        return user


    class Meta:
        model = User
        fields = ('current_password', 'password1', 'password2')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        required_css_class = 'required'
        self.users_cache = User.objects.filter(
            email__iexact=email,
            is_active=True
        )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        required_css_class = 'required'
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(_("Password reset on %s") % site_name,
                      t.render(Context(c)), from_email, [user.email])

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    new_password1 = forms.CharField(label=("New password"), required=True,
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label=("Confirm password"), required=True,
                                    widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "Please make sure the two password fields match.",
                    code='password_mismatch',
                )
        return password2

class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        required_css_class = 'required'
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return old_password
PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']

class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput)
    required_css_class = 'required'

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        required_css_class = 'required'
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user

class UserProfileForm(forms.ModelForm):
    """
    A Form For Editing a User Profile

    """
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        #if kwargs.get('instance'):
        #if kwargs['instance'].lab is not None:
        #    self.fields['lab'].queryset = Lab.objects.get(lab=kwargs['instance'].lab)
        #if kwargs['instance'].division is not None:
        #    self.fields['division'].queryset = Division.objects.get(division=kwargs['instance'].division)
        #if kwargs['instance'].branch is not None:
        #    self.fields['branch'].queryset = Branch.objects.get(branch=kwargs['instance'].branch)

    required_css_class = 'required'

    email_address_epa = forms.CharField(label="EPA Email Address", widget=forms.TextInput(), required=False)
    email_address_other = forms.CharField(label="Alternate Email Address", widget=forms.TextInput(), required=False)

    class Meta:
        model = UserProfile
        fields = ("email_address_epa", "email_address_other")

#class UserProfileAdminForm(forms.ModelForm):
#    """
#    A Form For Editing a User Profile
#
#    """
#    def __init__(self, *args, **kwargs):
#        super(UserProfileAdminForm, self).__init__(*args, **kwargs)
#        #if kwargs.get('instance'):
#        #if kwargs['instance'].lab is not None:
#        #    self.fields['lab'].queryset = Lab.objects.get(lab=kwargs['instance'].lab)
#        #if kwargs['instance'].division is not None:
#        #    self.fields['division'].queryset = Division.objects.get(division=kwargs['instance'].division)
#        #if kwargs['instance'].branch is not None:
#        #    self.fields['branch'].queryset = Branch.objects.get(branch=kwargs['instance'].branch)
#
#    required_css_class = 'required'
#    user_type = forms.ChoiceField(label=_("User Security Level"), choices=USER_TYPE_CHOICES, widget=forms.Select(), required=True)
#    can_edit = forms.ChoiceField(label="Can Edit", choices=YN_CHOICES, widget=forms.Select(), required=False)
#    can_create_users = forms.ChoiceField(label="Can Create Users", choices=YN_CHOICES, widget=forms.Select(), required=False)
#    #is_reviewer = forms.ChoiceField(label=_("Is A Reviewer"), choices=YN_CHOICES, widget=forms.Select(), required=True)
#    user_lab_one = forms.CharField(label=_("Users' Primary Lab Abbreviation"), widget=forms.TextInput(), required=False)
#    user_division_one = forms.CharField(label=_("Users' Primary Division Abbreviation"), widget=forms.TextInput(), required=False)
#    user_branch_one = forms.CharField(label=_("Users' Primary Branch Abbreviation"), widget=forms.TextInput(), required=False)
#    code_kept = forms.CharField(label=_("Password For Relookup - Optional"), widget=forms.TextInput(), required=False)
#
#    email_address_epa = forms.CharField(label="EPA Email Address", widget=forms.TextInput(), required=False)
#    email_address_other = forms.CharField(label="Alternate Email Address", widget=forms.TextInput(), required=False)
#
#    class Meta:
#        model = UserProfile
#        fields = ("user_type", "can_edit", "can_create_users", "user_lab_one", "user_division_one","user_branch_one", "code_kept", "email_address_epa", "email_address_other")

class RequestSubjectForm(forms.ModelForm):
    """
    A Form For Editing a User Profile

    """
    def __init__(self, *args, **kwargs):
        super(RequestSubjectForm, self).__init__(*args, **kwargs)
    required_css_class = 'required'
    the_name = forms.CharField(label=_("Users' Primary Lab Abbreviation"), widget=forms.TextInput(), required=False)
    email_address = forms.CharField(label=_("Users' Primary Division Abbreviation"), widget=forms.TextInput(), required=False)

    class Meta:
        model = RequestSubject
        fields = ("the_name", "email_address")

class ContactRequestForm(forms.ModelForm):
    """
    A Form For ContactRequest Used on Page 1

    """
    def __init__(self, *args, **kwargs):
        super(ContactRequestForm, self).__init__(*args, **kwargs)
        self.fields['request_subject'].queryset = RequestSubject.objects.filter(is_active="Y")

    required_css_class = 'required'
    the_name = forms.CharField(label=_("Name (required)"), widget=forms.TextInput(), required=True)
    email_address = forms.CharField(label=_("Email address (required)"), widget=forms.TextInput(), required=True)
    request_subject = forms.ModelChoiceField(label=_("Subject"), queryset=RequestSubject.objects.none(), widget=forms.Select(), required=False)

    the_description = forms.CharField(label=_("More information"), widget=forms.Textarea(), required=False)

    class Meta:
        model = ContactRequest
        fields = ("the_name", "email_address", "request_subject", "the_description")



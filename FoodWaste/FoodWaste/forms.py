# forms.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""Definition of forms."""

from accounts.models import User
from constants.models import YES_OR_NO
from django.forms import CharField, ModelForm, TextInput, Textarea, \
    PasswordInput, ModelMultipleChoiceField, SelectMultiple, BooleanField, \
    RadioSelect, FileField, ClearableFileInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from FoodWaste.models import SecondaryExistingData
#from phonenumber_field.formfields import PhoneNumberField
from teams.models import TeamMembership, Team

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""

    username = CharField(max_length=254,
                         widget=TextInput({
                             'class': 'form-control',
                             'placeholder': 'User name'}))
    password = CharField(label=_("Password"),
                         widget=PasswordInput({
                             'class': 'form-control',
                             'placeholder':'Password'}))


class SecondaryExistingDataForm(ModelForm):
    """Form for creating a new Existing Data Tracking instance."""

    teams = ModelMultipleChoiceField(
        widget=SelectMultiple({'class': 'form-control mb-2',
                               'placeholder': 'Teams'}),
        queryset=Team.objects.none(),
        label=_("Share With Teams"), required=False)

    work = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Work Office/Lab'}),
        label=_("User Work Office/Lab"), required=True)

    email = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Email'}),
        label=_("Email Address"), required=True)

    #phone = PhoneNumberField(
    #    widget=TextInput({'class': 'form-control mb-2',
    #                      'placeholder': '(555) 555-5555 or 555-555-5555'}),
    #    label=_("Phone Number"), required=True)
    phone = CharField(
        max_length=32,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': '(555) 555-5555 or 555-555-5555'}),
        label=_("Phone Number"), required=True)

    search = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Search Term'}),
        label=_("Search for Existing Data"), required=True)

    article_title = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Paste Article Title Here'}),
        label=_("Article Title"), required=True)

    disclaimer_req = BooleanField(label=_("EPA Discaimer Required"),
                                  required=False,
                                  initial=False,
                                  widget=RadioSelect(choices=YES_OR_NO))

    citation = CharField(
        max_length=255,
        widget=Textarea({'rows': 2, 'class': 'form-control mb-2',
                         'placeholder': 'APA Citation'}),
        label=_("APA Citation"), required=True)

    comments = CharField(
        max_length=255,
        widget=Textarea({'rows': 2, 'class': 'form-control mb-2',
                         'placeholder': 'Comments'}),
        label=_("Comments"), required=False)

    # TODO File Upload
    attachments = FileField(label=_("Upload File Attachments"), required=False,
                            widget=ClearableFileInput(
                                attrs={'multiple': False,
                                       'class': 'custom-file-input'}))

    def __init__(self, *args, **kwargs):
        """Override default init to add custom queryset for teams."""
        current_user = kwargs.pop('user')
        super(SecondaryExistingDataForm, self).__init__(*args, **kwargs)
        team_ids = TeamMembership.objects.filter(member=current_user).values_list('team', flat=True)
        self.fields['teams'].queryset = Team.objects.filter(id__in=team_ids)
        self.fields['teams'].label_from_instance = lambda obj: "%s" % obj.name

    class Meta:
        """Meta data for Existing Data Tracking."""
        model = SecondaryExistingData
        fields = ('work', 'email', 'phone', 'search', 'article_title',
                  'citation', 'comments')

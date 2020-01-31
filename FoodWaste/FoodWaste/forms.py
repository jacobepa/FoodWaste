# forms.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=W0613,E1101,R0903,W0611,C0411

"""Definition of forms."""

from django.forms import CharField, ChoiceField, ModelForm, TextInput, \
    Textarea, PasswordInput, ModelMultipleChoiceField, SelectMultiple, \
    BooleanField, RadioSelect, FileField, ClearableFileInput, \
    ModelChoiceField, Select, DateTimeField
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from constants.models import QA_CATEGORY_CHOICES, XMURAL_CHOICES, YES_OR_NO
from FoodWaste.models import  Division, ExistingData, ExistingDataSource, \
    QualityAssuranceProjectPlan, QappApproval
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
                             'placeholder': 'Password'}))


class QualityAssuranceProjectPlanForm(ModelForm):
    """Form for creating a new QAPP (Quality Assurance Project Plan)"""
    
    division = ModelChoiceField(
        label=_("Division:"), queryset=Division.objects.all(),
        widget=Select(attrs={'class': 'form-control mb-2'}), initial=0)

    division_branch = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Division Branch:"), required=True)

    title = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("QAPP Title:"), required=True)

    # Dynamic number of project leads

    qa_category = ChoiceField(
        label=_("QA Category:"), choices=QA_CATEGORY_CHOICES,
        widget=Select(attrs={'class': 'form-control mb-2'}), required=False)

    intra_extra = ChoiceField(
        label=_("Intra/Extramural:"), choices=XMURAL_CHOICES,
        widget=Select(attrs={'class': 'form-control mb-2'}), required=False)

    revision_number = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Revision Number:"), required=True)

    date = DateTimeField(
        label=_("Date:"),
        required=False,
        widget=DateTimeInput(attrs={'class': 'form-control mb-2'}))

    prepared_by = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Prepared By:"), required=True)

    strap = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("StRAP:"), required=True)

    tracking_id = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("QA Tracking ID:"), required=True)

    class Meta:
        """Meta data for QAPP Form."""

        model = QualityAssuranceProjectPlan
        fields = ('division', 'division_branch', 'title', 'qa_category',
                  'intra_extra', 'revision_number', 'date', 'prepared_by',
                  'strap', 'tracking_id')


class QappApprovalForm(ModelForm):
    """Form for creating the QAPP Approval page"""

    project_plan_title = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    activity_number = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Activity Number"), required=True)

    # TODO: Handle this carefully. It's not user defined, but rather based on
    #       the QAPP creation flow. This form will always be instantiated with
    #       the QAPP ID passed in.
    qapp = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2', 'readonly': True}),
        label=_(""), required=True)

    class Meta:
        """Meta data for QAPP Form."""

        model = QappApproval
        fields = ('project_plan_title', 'activity_number', 'qapp')


class ExistingDataForm(ModelForm):
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

    source = ModelChoiceField(
        label=_("Source"), queryset=ExistingDataSource.objects.all(),
        widget=Select(attrs={'class': 'form-control mb-2'}), initial=0)

    source_title = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Source Title'}),
        label=_("Source Title"), required=True)

    keywords = CharField(
        max_length=1024,
        widget=Textarea({'rows': 2, 'class': 'form-control mb-2',
                         'placeholder': 'Keywords, Comma Seperated'}),
        label=_("Keywords"), required=False)

    url = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'https://www.epa.gov/'}),
        label=_("Source URL Link"), required=True)

    disclaimer_req = BooleanField(label=_("EPA Discaimer Required"),
                                  required=False,
                                  initial=False,
                                  widget=RadioSelect(choices=YES_OR_NO))

    citation = CharField(
        max_length=2048,
        widget=Textarea({'rows': 3, 'class': 'form-control mb-2',
                         'placeholder': 'Citation'}),
        label=_("Citation"), required=True)

    comments = CharField(
        max_length=2048,
        widget=Textarea({'rows': 3, 'class': 'form-control mb-2',
                         'placeholder': 'Comments'}),
        label=_("Comments"), required=False)

    attachments = FileField(label=_("Upload File Attachments"), required=False,
                            widget=ClearableFileInput(
                                attrs={'multiple': False,
                                       'class': 'custom-file-input'}))

    def __init__(self, *args, **kwargs):
        """Override default init to add custom queryset for teams."""
        try:
            current_user = kwargs.pop('user')
            super(ExistingDataForm, self).__init__(*args, **kwargs)
            team_ids = TeamMembership.objects.filter(
                member=current_user).values_list('team', flat=True)
            self.fields['teams'].queryset = Team.objects.filter(id__in=team_ids)
            self.fields['teams'].label_from_instance = lambda obj: "%s" % obj.name
        except:
            super(ExistingDataForm, self).__init__(*args, **kwargs)

    class Meta:
        """Meta data for Existing Data Tracking."""

        model = ExistingData
        fields = ('work', 'email', 'phone', 'search', 'source',
                  'source_title', 'keywords', 'url',
                  'citation', 'comments')

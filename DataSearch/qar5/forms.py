# forms.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of forms."""

from django.forms import CharField, ChoiceField, ModelForm, TextInput, \
    Textarea, PasswordInput, ModelMultipleChoiceField, SelectMultiple, \
    BooleanField, RadioSelect, FileField, ClearableFileInput, \
    ModelChoiceField, Select, DateTimeField, inlineformset_factory
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from constants.models import QA_CATEGORY_CHOICES, XMURAL_CHOICES, YES_OR_NO
from qar5.models import Division, Qapp, QappApproval, QappLead

class QappForm(ModelForm):
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
    # project_leads = inlineformset_factory()

    qa_category = ChoiceField(
        label=_("QA Category:"), choices=QA_CATEGORY_CHOICES,
        widget=Select(attrs={'class': 'form-control mb-2'}), required=True)

    intra_extra = ChoiceField(
        label=_("Intra/Extramural:"), choices=XMURAL_CHOICES,
        widget=Select(attrs={'class': 'form-control mb-2'}), required=True)

    revision_number = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Revision Number:"), required=True)

    date = DateTimeField(
        label=_("Date:"),
        required=True,
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

        model = Qapp
        fields = ('division', 'division_branch', 'title', 'qa_category',
                  'intra_extra', 'revision_number', 'date', 'prepared_by',
                  'strap', 'tracking_id')


class QappLeadForm(ModelForm):
    """Form for creating project leads for a given qapp"""

    name = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Lead Name:"), required=True)

    qapp = ModelChoiceField(queryset=Qapp.objects.all(), initial=0,
                               required=True, label=_("Parent QAPP"),
                               widget=TextInput(attrs={'class': 'form-control mb-2',
                                                       'readonly':'readonly'}))

    class Meta:
        """Meta data for QAPP Form."""

        model = QappLead
        fields = ('name', 'qapp')


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

    qapp = ModelChoiceField(queryset=Qapp.objects.all(), initial=0,
                               required=True, label=_("Parent QAPP"),
                               widget=TextInput(attrs={'class': 'form-control mb-2',
                                                       'readonly':'readonly'}))

    class Meta:
        """Meta data for QAPP Form."""

        model = QappApproval
        fields = ('project_plan_title', 'activity_number', 'qapp')


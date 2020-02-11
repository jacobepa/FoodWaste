# forms.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of forms."""

from django.forms import CharField, ChoiceField, ModelForm, TextInput, \
    Textarea, PasswordInput, ModelMultipleChoiceField, SelectMultiple, \
    BooleanField, RadioSelect, FileField, ClearableFileInput, \
    ModelChoiceField, Select, DateTimeField, inlineformset_factory, \
    CheckboxInput
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from constants.models import QA_CATEGORY_CHOICES, XMURAL_CHOICES, YES_OR_NO
from constants.qar5 import SECTION_B_INFO
from qar5.models import Division, Qapp, QappApproval, QappLead, \
    QappApprovalSignature, SectionB

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
                               widget=TextInput(
                                   attrs={'class': 'form-control mb-2',
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
                               widget=TextInput(
                                   attrs={'class': 'form-control mb-2',
                                          'readonly':'readonly'}))

    class Meta:
        """Meta data for QappApproval Form."""

        model = QappApproval
        fields = ('project_plan_title', 'activity_number', 'qapp')


class QappApprovalSignatureForm(ModelForm):
    """Form for creating the QAPP Approval Signatures"""

    qapp_approval = ModelChoiceField(
        queryset=QappApproval.objects.all(), initial=0,
        required=True, label=_("Parent QAPP Approval"),
        widget=TextInput(attrs={'class': 'form-control mb-2',
                                'readonly':'readonly'}))

    contractor = BooleanField(
        required=False, label=_("Contractor Signature? Default (no check) is EPA."),
        widget=CheckboxInput(
            attrs={'class': 'form-control custom-control-input'}))

    name = CharField(max_length=255,
                     widget=TextInput({'class': 'form-control mb-2'}),
                     label=_("Print Name:"), required=False)

    signature = CharField(
        max_length=255, label=_("Signature:"), required=False,
        widget=TextInput({'class': 'form-control mb-2',
                          'readonly': 'readonly'}))

    date = CharField(
        max_length=255, label=_("Date:"), required=False,
        widget=TextInput({'class': 'form-control mb-2',
                          'readonly': 'readonly'}))

    class Meta:
        """Meta data for QappApprovalSignature Form."""

        model = QappApprovalSignature
        fields = ('qapp_approval', 'contractor', 'name', 'signature', 'date')


class SectionBForm(ModelForm):
    """Class representing the entirety of SectionB for a given QAPP"""
    qapp = ModelChoiceField(queryset=Qapp.objects.all(), initial=0,
                               required=True, label=_("Parent QAPP"),
                               widget=TextInput(
                                   attrs={'class': 'form-control mb-2',
                                          'readonly':'readonly'}))
    # B1 Secondary Data will be a dropdown with options from the following: ?
    # analytical methods, animal subjects, cell culture models, existing data,
    # measurements, model application, model development, software development
    #b1_secondary_data = 

    # TODO: Add constant text as info pop up (potentially help_text ?)
    b1_existing_data = CharField(
        max_length=255, help_text=SECTION_B_INFO[2],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b1_data_requirements = CharField(
        max_length=255, help_text=SECTION_B_INFO[3],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b1_databases_maps_literature = CharField(
        max_length=255, help_text=SECTION_B_INFO[4],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b1_non_quality_constraints = CharField(
        max_length=255, help_text=SECTION_B_INFO[5],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b2_secondary_data_sources = CharField(
        max_length=255, help_text=SECTION_B_INFO[6],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b2_process = CharField(
        max_length=255, help_text=SECTION_B_INFO[7],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b2_rationale = CharField(
        max_length=255, help_text=SECTION_B_INFO[8],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b2_procedures = CharField(
        max_length=255, help_text=SECTION_B_INFO[9],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b2_disclaimer = CharField(
        max_length=255, help_text=SECTION_B_INFO[10],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b3_process = CharField(
        max_length=255, help_text=SECTION_B_INFO[11],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)

    b4_existing_data_tracking = CharField(
        max_length=255, help_text=SECTION_B_INFO[12],
        widget=TextInput({'class': 'form-control mb-2'}),
        label=_("Project Plan Title"), required=True)
    
    class Meta:
        """Meta data for QappApprovalSignature Form."""

        model = SectionB
        fields = ('b1_existing_data', 'b1_data_requirements',
                  'b1_databases_maps_literature', 'b1_non_quality_constraints',
                  'b2_secondary_data_sources', 'b2_process', 'b2_rationale',
                  'b2_procedures', 'b2_disclaimer', 'b3_process',
                  'b4_existing_data_tracking')

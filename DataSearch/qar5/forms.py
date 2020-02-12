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
from constants.qar5 import SECTION_A_INFO
from qar5.models import Division, Qapp, QappApproval, QappLead, \
    QappApprovalSignature, SectionA, SectionB, SectionD

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


class SectionAForm(ModelForm):
    """Class representing the rest of Section A (A.3 and later)"""
    qapp = ModelChoiceField(queryset=Qapp.objects.all(), initial=0,
                               required=True, label=_("Parent QAPP"),
                               widget=Textarea(
                                   attrs={'class': 'form-control mb-2',
                                          'readonly':'readonly'}))
    a3 = CharField(
        max_length=2047, label=_("A.3 Distribution List"),
        required=False, widget=Textarea(
            {'class': 'form-control mb-2', 'readonly': 'readonly'}),
        initial=SECTION_A_INFO['a3'])

    a4 = CharField(
        max_length=2047, label=_("A.4 Project Task Organization"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    a4_chart = FileField(
        label=_("Upload Organizational Chart (optional)"), required=False,
        widget=ClearableFileInput(attrs={
            'multiple': False, 'class': 'custom-file-input'}))

    a5 = CharField(
        max_length=2047, label=_("A.5 Problem Definition Background"),
        required=True, widget=Textarea(
            {'class': 'form-control mb-2'}))

    a6 = CharField(
        max_length=2047, label=_("A.6 Project Description"),
        required=True, widget=Textarea(
            {'class': 'form-control mb-2'}))

    a7 = CharField(
        max_length=2047, label=_("A.7 Quality Objectives and Criteria"),
        required=True, widget=Textarea(
            {'class': 'form-control mb-2'}))

    a8 = CharField(
        max_length=2047, label=_("A.8 Special Training Certification"),
        required=True, widget=Textarea(
            {'class': 'form-control mb-2'}))

    a9 = CharField(
        max_length=255, label=_("A.9 Documents and Records"),
        required=False, widget=Textarea(
            {'class': 'form-control mb-2', 'readonly': 'readonly'}),
        initial=SECTION_A_INFO['a9'])

    a9_drive_path = CharField(
        max_length=255, label=_("A.9 Drive Path:"), required=True,
        widget=TextInput({'class': 'form-control mb-2'}))
    
    class Meta:
        """Meta data for SectionAForm Form."""

        model = SectionA
        fields = ('qapp', 'a3', 'a4', 'a4_chart', 'a5',
                  'a6', 'a7', 'a8', 'a9', 'a9_drive_path')


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
    #b1_1 = 

    # TODO: Add constant text as info pop up (potentially help_text ?)
    b1_2 = CharField(
        max_length=2047, label=_("B.1 Describe Existing Data Use"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b1_3 = CharField(
        max_length=2047, label=_("B.1 Specify Requirements"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b1_4 = CharField(
        max_length=2047, label=_("B.1 Identify Databases, Maps, Literature..."),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b1_5 = CharField(
        max_length=2047, label=_("B.1 Identify Non-Quality Constraints"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b2_1 = CharField(
        max_length=2047, label=_("B.2 Identify Sources"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b2_2 = CharField(
        max_length=2047, label=_("B.2 Describe Acceptance/Rejection Process"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b2_3 = CharField(
        max_length=2047, label=_("B.2 Discuss Rationale for Selections"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b2_4 = CharField(
        max_length=2047, label=_("B.2 Describe Procedures"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b2_5 = CharField(
        max_length=2047, label=_("B.2 Disclaimer"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b3 = CharField(
        max_length=2047, label=_("B.3 Data Management and Documentation"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))

    b4 = CharField(
        max_length=2047, label=_("B.4 Existing Data Tracking"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))
    
    class Meta:
        """Meta data for SectionBForm Form."""

        model = SectionB
        fields = ('b1_2', 'b1_3', 'b1_4', 'b1_5', 'b2_1', 'b2_2',
                  'b2_3', 'b2_4', 'b2_5', 'b3', 'b4')
         

# No SectionC Necessary, both fields are auto-generated.

class SectionDForm(ModelForm):
    """Class representing the entirety of SectionD for a given QAPP"""
    qapp = ModelChoiceField(queryset=Qapp.objects.all(), initial=0,
                               required=True, label=_("Parent QAPP"),
                               widget=TextInput(
                                   attrs={'class': 'form-control mb-2',
                                          'readonly':'readonly'}))
    
    d1 = CharField(
        max_length=2047,
        label=_("D.1 Data Review, Verification, and Validation"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))
    
    d2 = CharField(
        max_length=2047, label=_("D.2 Verification and Validation Methods"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))
    
    d3 = CharField(
        max_length=2047,
        label=_("D.3 Reconciliation with User Requirements"),
        required=True, widget=Textarea({'class': 'form-control mb-2'}))


    class Meta:
        """Meta data for SectionBForm Form."""

        model = SectionD
        fields = ('d1', 'd2', 'd3')
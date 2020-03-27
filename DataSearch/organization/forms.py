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
from constants.utils import *
from django.db.models import Q
from organization.models import *

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import check_password, make_password
import datetime

class UserModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name + " (" + obj.email + ")"


class OfficeForm(forms.ModelForm):
    """
    A Form For Creating/Editing an Office
    """
    required_css_class = 'required'

    def __init__(self, is_editable, *args, **kwargs):
        self.is_editable = is_editable
        super(OfficeForm, self).__init__(*args, **kwargs)

        async_filters = {
            "qams": (User, Q(userprofile__display_in_dropdowns="Y")),
            }
        setQuerySets(self, async_filters, kwargs)

        if not self.is_editable:
            for field in self.Meta.fields:
                self.fields[field].widget.attrs['disabled'] = True

    office = forms.CharField(label=_("Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    description = forms.CharField(label=_("Description"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    url = forms.CharField(label=_("URL"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)

    qams = UserModelMultipleChoiceField(label=_("QA Managers"),
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control jasc-user-select',
                       'data-placeholder': 'Search people . . .'}),
            queryset=User.objects.none(),
            required=False,
            help_text='')


    class Meta:
        model = Office
        fields = ("office", "abbreviation", "description", "url","qams")


class LabForm(forms.ModelForm):
    """
    A Form For Creating/Editing a Lab, now called Center
    """
    required_css_class = 'required'

    def __init__(self, is_editable, office=None, *args, **kwargs):
        self.is_editable = is_editable
        super(LabForm, self).__init__(*args, **kwargs)
        if office:
            self.fields['office'].queryset = Office.objects.filter(id=office.id)
            self.fields['office'].initial = office

        async_filters = {
            "qams": (User, Q(userprofile__display_in_dropdowns="Y")),
            }
        setQuerySets(self, async_filters, kwargs)

        if not self.is_editable:
            for field in self.Meta.fields:
                self.fields[field].widget.attrs['disabled'] = True

    lab = forms.CharField(label=_("Center Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    description = forms.CharField(label=_("Description"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    url = forms.CharField(label=_("URL"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    office = forms.ModelChoiceField(label=_("Office"), queryset=Office.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    designation_code = forms.CharField(label=_("Designation Code"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)

    is_active = forms.BooleanField(label=_("Active"), widget=forms.CheckboxInput(attrs={'class': 'is_active_checkbox'}),
                                   required=False)

    qams = UserModelMultipleChoiceField(label=_("QA Managers"),
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control jasc-user-select',
                       'data-placeholder': 'Search people . . .'}),
            queryset=User.objects.none(),
            required=False,
            help_text='')

    class Meta:
        model = Lab
        fields = ("lab", "abbreviation", "description", "url", "designation_code", "office", "is_active","qams")


class DivisionForm(forms.ModelForm):
    """
    A Form For Creating/Editing a Division
    """
    required_css_class = 'required'

    def __init__(self, is_editable, lab=None, *args, **kwargs):
        self.is_editable = is_editable
        super(DivisionForm, self).__init__(*args, **kwargs)
        if lab:
            self.fields['lab'].queryset =Lab.objects.filter(id=lab.id)
            self.fields['lab'].initial = lab

        async_filters = {
            "qams": (User, Q(userprofile__display_in_dropdowns="Y")),
            }
        setQuerySets(self, async_filters, kwargs)

        if not self.is_editable:
            for field in self.Meta.fields:
                self.fields[field].widget.attrs['disabled'] = True

    division = forms.CharField(label=_("Division Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    description = forms.CharField(label=_("Description"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    url = forms.CharField(label=_("URL"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    lab = forms.ModelChoiceField(label=_("Center"), queryset=Lab.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    is_active = forms.BooleanField(label=_("Active"), widget=forms.CheckboxInput(attrs={'class': 'is_active_checkbox'}), required=False)

    qams = UserModelMultipleChoiceField(label=_("QA Managers"),
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control jasc-user-select',
                       'data-placeholder': 'Search people . . .'}),
            queryset=User.objects.none(),
            required=False,
            help_text='')


    class Meta:
        model = Division
        fields = ("division", "abbreviation", "description", "url", "lab", "is_active","qams")


class BranchForm(forms.ModelForm):
    """
    A Form For Creating/Editing an Branch
    """
    required_css_class = 'required'

    def __init__(self, is_editable, lab=None, division=None, *args, **kwargs):
        self.is_editable = is_editable
        super(BranchForm, self).__init__(*args, **kwargs)
        if lab:
            self.fields['division'].queryset = Division.objects.filter(lab__id=lab.id)
        if division:
            self.fields['division'].initial = division
            self.fields['division'].queryset = Division.objects.filter(id=division.id)

        async_filters = {
            "qams": (User, Q(userprofile__display_in_dropdowns="Y")),
            }
        setQuerySets(self, async_filters, kwargs)


        if not self.is_editable:
            for field in self.Meta.fields:
                self.fields[field].widget.attrs['disabled'] = True

    branch = forms.CharField(label=_("Branch Name"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    abbreviation = forms.CharField(label=_("Abbreviation"), widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    description = forms.CharField(label=_("Description"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                                  required=False)
    url = forms.CharField(label=_("URL"), widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    division = forms.ModelChoiceField(label=_("Division"), queryset=Division.objects.all(),
                                 widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    is_active = forms.BooleanField(label=_("Active"), widget=forms.CheckboxInput(attrs={'class': 'is_active_checkbox'}),
                                   required=False)

    qams = UserModelMultipleChoiceField(label=_("QA Managers"),
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control jasc-user-select',
                       'data-placeholder': 'Search people . . .'}),
            queryset=User.objects.none(),
            required=False,
            help_text='')


    class Meta:
        model = Branch
        fields = ("branch", "abbreviation", "description", "url", "division", "is_active","qams")


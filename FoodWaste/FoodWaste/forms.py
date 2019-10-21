# forms.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""Definition of forms."""

from django.forms import CharField, ModelForm, TextInput, Textarea, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from FoodWaste.models import TrackingTool
from phonenumber_field.formfields import PhoneNumberField

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


class TrackingToolForm(ModelForm):
    """Form for creating a new Secondary / Existing Data Tracking instance."""

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
    phone = PhoneNumberField(
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': '555-555-5555'}),
        label=_("Phone Number"), required=True)
    search = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Search Term'}),
        label=_("Search for Secondary / Existing Data"), required=True)
    article_title = CharField(
        max_length=255,
        widget=TextInput({'class': 'form-control mb-2',
                          'placeholder': 'Paste Article Title Here'}),
        label=_("Article Title"), required=True)
    # Date accessed should be automatically generated as NOW by the model.
    # date_accessed =
    comments = CharField(
        max_length=255,
        widget=Textarea({'rows': 3, 'class': 'form-control mb-2',
                         'placeholder': 'Comments'}),
        label=_("Comments"), required=False)

    class Meta:
        """Meta data for Secondary / Existing Data Tracking."""

        model = TrackingTool
        fields = ()

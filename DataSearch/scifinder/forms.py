# forms.py (scifinder)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=W0613,E1101,R0903,W0611,C0411

"""Definition of forms."""

from django.forms import ModelForm, FileField, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from scifinder.models import Upload


class UploadForm(ModelForm):
    """Form that handles SciFinder attachment uploads."""

    file = FileField(
        label=_("Upload one File at a time"),
        required=True,
        widget=ClearableFileInput(attrs={
            'multiple': False,
            'class': 'usa-file-input'
        }))

    class Meta:
        """Meta class to specify the base model and fields to implement."""

        model = Upload
        fields = ('file', )

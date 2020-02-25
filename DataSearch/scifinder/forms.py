# forms.py (scifinder)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=W0613,E1101,R0903,W0611,C0411

"""Definition of forms."""

from django.forms import ModelForm
from scifinder.models import Upload


class UploadForm(ModelForm):
    """Add docstring."""  # TODO add docstring.

    class Meta:
        """Add docstring."""  # TODO add docstring.

        model = Upload
        fields = ('file', )

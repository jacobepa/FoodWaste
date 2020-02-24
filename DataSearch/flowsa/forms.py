# forms.py (flowsa)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=W0613,E1101,R0903,W0611,C0411

"""Definition of forms."""

from django.forms import ModelForm
from flowsa.models import Upload


class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('file', )
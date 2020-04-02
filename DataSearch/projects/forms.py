# forms.py (projects)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=R0903

"""
Forms for managing projects.

Available functions:
- Form For Creating or Updating a Project
"""

from django import forms
# from django.utils.translation import ugettext_lazy as _
# from projects.models import Project


# class TeamManagementForm(forms.ModelForm):
#     """Form For Creating or Updating a Project."""

#     # Name of the project
#     name = forms.CharField(label=_("Name"),
#                            help_text="Project names must be unique",
#                            widget=forms.TextInput(
#                                attrs={'class': 'form-control'}), required=True)

#     class Meta:
#         """Meta data for the Project Management Form."""

#         model = Project
#         fields = ("name",)

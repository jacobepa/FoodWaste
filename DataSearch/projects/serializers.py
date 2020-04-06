# serializers.py (projects)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301,R0903,E1101,W0221,W0613

"""
Project serializers.

Available functions:
- JSON serializer for Project list REST api
"""


from rest_framework import serializers
from projects.models import CenterOffice, Division, Branch


class CenterSerializer(serializers.ModelSerializer):
    """JSON serializer for Project list REST api."""

    class Meta:
        """Meta data related to the Project serializer."""

        model = CenterOffice
        fields = ('id', 'date_created', 'last_modified', 'name',
                  'weblink', 'description', 'office_id',)


class DivisionSerializer(serializers.ModelSerializer):
    """JSON serializer for Project list REST api."""

    class Meta:
        """Meta data related to the Project serializer."""

        model = Division
        fields = ('id', 'date_created', 'last_modified', 'name',
                  'weblink', 'description', 'center_office_id',
                  'office_id',)


class BranchSerializer(serializers.ModelSerializer):
    """JSON serializer for Project list REST api."""

    class Meta:
        """Meta data related to the Project serializer."""

        model = Branch
        fields = ('id', 'date_created', 'last_modified', 'name',
                  'weblink', 'description', 'center_office_id',
                  'division_id', 'office_id',)

# models.py (projects)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""
Models for projects of users.

Available functions:
- Project object allows groups of users to share projects
- Object describing user's membership on a project project
"""

from django.contrib.auth.models import User
from django.db import models
from teams.models import Team


class Office(models.Model):
    """ TODO """
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    weblink = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class OfficeCenter(models.Model):
    """ TODO """
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    weblink = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class Division(models.Model):
    """ TODO """
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    weblink = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    #lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class Branch(models.Model):
    """ TODO """
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    weblink = models.CharField(blank=True, null=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    #lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class OrdRap(models.Model):
    """ TODO """
    name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.name


class Project(models.Model):
    """TODO Docstring"""

    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    # TODO: Center/Office ? Is this the same as Lab in QA TRACK?
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(blank=False, max_length=255, db_index=True)
    # Team Members (List of teams related to this project)
    teams = models.ManyToManyField(Team, through='ProjectSharingTeamMap')
    ord_rap = models.ForeignKey(OrdRap, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """Override str method to display name instead of stringified obj."""
        return self.title


class ProjectSharingTeamMap(models.Model):
    """Mapping between Projects and Teams they share."""

    added_date = models.DateTimeField(
        auto_now_add=True, blank=False, editable=False)
    project = models.ForeignKey(
        Project, blank=False, related_name='project_teams',
        on_delete=models.CASCADE)
    team = models.ForeignKey(
        Team, blank=False, related_name='team_project',
        on_delete=models.CASCADE)
    # Indicates if the team can edit the project.
    can_edit = models.BooleanField(blank=False, default=True)

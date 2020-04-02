# admin.py (projects)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""
Define classes used to generate Django Admin portion of the website.

Available functions:
- Sets Projects
- Sets Project Memberships
"""

from django.contrib import admin
# from projects.models import Project, TeamMembership


# class TeamAdmin(admin.ModelAdmin):
#     """Custom Admin class for managing Projects."""

#     model = Project
#     fields = ('name',)
#     readonly_fields = ('created_date', 'created_by', 'last_modified_date',
#                        'last_modified_by', 'members',)

#     def save_model(self, request, obj, form, change):
#         """Custom save method to attach created_by user."""
#         try:
#             temp_obj = obj.created_by
#         except:
#             obj.created_by = request.user
#         obj.last_modified_by = request.user
#         obj.save()


# admin.site.register(Project, TeamAdmin)

# admin.site.register(TeamMembership)

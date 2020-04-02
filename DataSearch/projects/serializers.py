# # serializers.py (projects)
# # !/usr/bin/env python3
# # coding=utf-8
# # young.daniel@epa.gov
# # py-lint: disable=C0301,R0903,E1101,W0221,W0613

# """
# Project serializers.

# Available functions:
# - JSON serializer for reading project members
# - Serializer for create, update, delete
# - JSON serializer for Project list REST api
# """


# from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
# from django.utils import timezone
# from accounts.serializers import UserSerializer
# from projects.models import Project, TeamMembership, User


# class TeamMembershipSerializer(serializers.ModelSerializer):
#     """JSON serializer for reading project members."""

#     member = UserSerializer(many=False)

#     class Meta:
#         """Meta data related to the Project Membership serializer."""

#         model = TeamMembership
#         fields = ('id', 'added_date', 'is_owner', 'can_edit', 'member')


# class TeamMembershipModifySerializer(serializers.ModelSerializer):
#     """Serializer for create, update, delete."""

#     project = serializers.PrimaryKeyRelatedField(many=False,
#                                               queryset=Project.objects.all())
#     member = serializers.PrimaryKeyRelatedField(many=False,
#                                                 queryset=User.objects.all())
#     id = serializers.IntegerField(required=False, read_only=True)
#     added_date = serializers.DateTimeField(required=False,
#                                            default=serializers.CreateOnlyDefault
#                                            (timezone.now))
#     is_owner = serializers.BooleanField(required=False,
#                                         default=serializers.CreateOnlyDefault(
#                                             False))
#     can_edit = serializers.BooleanField(required=False,
#                                         default=serializers.CreateOnlyDefault(
#                                             True))

#     def validate(self, data):
#         """Make sure we do not already have an owner."""
#         if "is_owner" in data and data["is_owner"]:
#             current_owner = TeamMembership.objects.filter(project=data["project"],
#                                                           is_owner=True).first()
#             if current_owner is not None:
#                 raise ValidationError("projects can only have one owner")
#         return data

#     class Meta:
#         """Meta data related to the Project Membership Modification serializer."""

#         model = TeamMembership
#         fields = ('id', 'added_date', 'is_owner', 'can_edit', 'member', 'project')


# class TeamSerializer(serializers.ModelSerializer):
#     """JSON serializer for Project list REST api."""

#     id = serializers.IntegerField(required=False, read_only=True)
#     created_by = UserSerializer(many=False, required=False,
#                                 default=serializers.CreateOnlyDefault(
#                                     serializers.CurrentUserDefault()))
#     created_date = serializers.DateTimeField(required=False,
#                                              default=serializers.CreateOnlyDefault(
#                                                  timezone.now))
#     last_modified_by = UserSerializer(many=False,
#                                       default=serializers.CurrentUserDefault())
#     last_modified_date = serializers.DateTimeField(required=False,
#                                                    default=timezone.now)
#     team_memberships = TeamMembershipSerializer(many=True, read_only=True,
#                                                 required=False)

#     class Meta:
#         """Meta data related to the Project serializer."""

#         model = Project
#         fields = ('id', 'name', 'created_date', 'created_by',
#                   'last_modified_date', 'last_modified_by', 'team_memberships')

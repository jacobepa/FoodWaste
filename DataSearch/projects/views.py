# # views.py (accounts)
# # !/usr/bin/env python3
# # coding=utf-8
# # young.daniel@epa.gov
# # py-lint: disable=C0301,R0901,E1101,R0912

# """
# Project management views.

# Available functions:
# - Create the form view
# - View to edit a project name
# - Project Management Form
# """

# from datetime import datetime
# from io import BytesIO
# from rest_framework.parsers import JSONParser
# from rest_framework.response import Response
# from rest_framework.views import APIView, status, Http404
# from rest_framework import permissions
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
# from django.shortcuts import render
# from django.views.generic import FormView, ListView
# from django.test.client import RequestFactory
# from accounts.models import User
# from projects.forms import TeamManagementForm, Project
# from projects.models import TeamMembership
# from projects.serializers import TeamSerializer, UserSerializer, \
#     TeamMembershipSerializer, TeamMembershipModifySerializer


# class TeamListView(LoginRequiredMixin, ListView):
#     """
#     New class to return a projects list view.

#     This will serve as the management view where users can view their projects,
#     edit their projects, and create new projects.
#     """

#     model = Project
#     context_object_name = 'projects'
#     template_name = 'team_list.html'

#     def get_queryset(self):
#         """Override default queryset with set of projects which requesting user is member."""
#         user = self.request.user
#         return Project.objects.filter(members=user).order_by(
#             'name').select_related(
#                 "created_by", "last_modified_by").prefetch_related(
#                     "team_memberships", "team_memberships__member").all()


# class TeamCreateView(FormView):
#     """Class containing the view to create a new project."""

#     form_class = TeamManagementForm
#     template = 'team_create.html'

#     @method_decorator(login_required)
#     def get(self, request, *args, **kwargs):
#         """Display the project create form."""
#         form = TeamManagementForm()
#         return render(request, self.template, {'form': form})

#     @method_decorator(login_required)
#     def post(self, request, *args, **kwargs):
#         """Save the changes to the user form."""
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             team_instance = form.save(commit=False)
#             # Project creator.
#             team_instance.created_by = request.user
#             # When and by whom the project was created.
#             date_now = datetime.now()
#             team_instance.created_date = date_now
#             team_instance.created_by = request.user
#             # When and by whom the project was last modified.
#             team_instance.last_modified_date = date_now
#             team_instance.last_modified_by = request.user
#             # Save the project
#             team_instance.save()

#             # Add a membership for the requesting user.
#             membership_instance = TeamMembership()
#             membership_instance.added_date = date_now
#             membership_instance.member = request.user
#             membership_instance.project = team_instance
#             membership_instance.is_owner = True
#             membership_instance.can_edit = True
#             membership_instance.save()

#             return HttpResponseRedirect(
#                 reverse('team_manage', kwargs={'team_id': team_instance.id}))

#         return render(request, self.template, locals())


# class TeamEditView(FormView):
#     """View to edit a project name."""

#     template = 'team_edit.html'
#     form_class = TeamManagementForm

#     @method_decorator(login_required)
#     def get(self, request, *args, **kwargs):
#         """Display the project create form."""
#         ctx = {}
#         ctx['team_id'] = kwargs["team_id"] if kwargs is not None and 'team_id' in kwargs else None
#         if ctx['team_id'] is not None:
#             ctx['team_data'] = APITeamDetailView.as_view()(
#                 request, team_id=ctx['team_id'], format='json').rendered_content
#             ctx['project'] = JSONParser().parse(BytesIO(ctx['team_data']))
#             return render(request, self.template, ctx)
#         return HttpResponseRedirect(reverse('dashboard'))

#     @method_decorator(login_required)
#     def post(self, request, *args, **kwargs):
#         """Save the changes to the user form."""
#         ctx = {}
#         ctx['params'] = request.POST
#         ctx['team_id'] = kwargs["team_id"] if kwargs is not None and 'team_id' in kwargs else None

#         if ctx['team_id'] is not None:
#             # Update the project name.
#             ctx['team_obj'] = Project.objects.get(id=ctx['team_id'])
#             if ctx['team_obj'] is not None:
#                 ctx['name'] = ctx['params']['name'] if 'name' in ctx['params'] else None
#                 ctx['name'] = ctx['name'].strip()
#                 if ctx['name'] is not None and ctx['name']:
#                     ctx['team_obj'].name = ctx['name']
#                     ctx['team_obj'].save()
#                 else:
#                     ctx['error_msg'] = "Invalid project name."
#             else:
#                 ctx['error_msg'] = "Invalid project id specified."

#             # Retrieve the updated data and render the view.
#             get_request = RequestFactory().get('/')
#             get_request.user = request.user
#             ctx['team_data'] = APITeamDetailView.as_view()(
#                 get_request, team_id=ctx['team_id'], format='json').rendered_content
#             ctx['project'] = JSONParser().parse(BytesIO(ctx['team_data']))
#             return render(request, self.template, ctx)

#         # We should never get here, so just redirect to the dashboard.
#         return HttpResponseRedirect(reverse('dashboard'))


# class TeamManagementView(FormView):
#     """Class containing methods to manage projects."""

#     template = 'team_manage.html'
#     form_class = TeamManagementForm

#     @method_decorator(login_required)
#     def get(self, request, *args, **kwargs):
#         """Display the project create form."""
#         ctx = {}
#         ctx['team_id'] = kwargs["team_id"] if kwargs is not None and 'team_id' in kwargs else None
#         if ctx['team_id'] is not None:
#             ctx['team_data'] = APITeamDetailView.as_view()(
#                 request, team_id=ctx['team_id'], format='json').rendered_content
#             ctx['project'] = JSONParser().parse(BytesIO(ctx['team_data']))
#             ctx['nonmembers_data'] = APITeamMembershipListView.as_view()(
#                 request, team_id=ctx['team_id'], nonmember=1, format='json').rendered_content
#             ctx['nonmembers'] = JSONParser().parse(BytesIO(ctx['nonmembers_data']))
#             return render(request, self.template, ctx)
#         return HttpResponseRedirect(reverse('dashboard'))

#     @method_decorator(login_required)
#     def post(self, request, *args, **kwargs):
#         """Save the changes to the user form."""
#         ctx = {}
#         ctx['params'] = request.POST
#         ctx['command'] = ctx['params']["command"] if "command" in ctx['params'] else None
#         ctx['team_id'] = kwargs["team_id"] if kwargs is not None and 'team_id' in kwargs else None

#         if ctx['team_id'] is not None and ctx['command'] is not None:
#             if ctx['command'] == 'adduser':
#                 # Add a user membership to the project.
#                 ctx['user_id'] = int(ctx['params']['user_id']) if 'user_id' in ctx['params'] else None
#                 if ctx['user_id'] is not None:
#                     # Check if the user already has a membership, this can
#                     # happen if the user reloads the page.
#                     ctx['membership_list'] = TeamMembership.objects.filter(
#                         team_id=ctx['team_id'], member_id=ctx['user_id']).all()
#                     if ctx['membership_list'] is None or not ctx['membership_list']:
#                         # Add a membership.
#                         ctx['team_obj'] = Project.objects.get(id=ctx['team_id'])
#                         ctx['member_obj'] = User.objects.get(id=ctx['user_id'])
#                         ctx['membership'] = TeamMembership()
#                         ctx['membership'].added_date = datetime.now()
#                         ctx['membership'].project = ctx['team_obj']
#                         ctx['membership'].member = ctx['member_obj']
#                         ctx['membership'].can_edit = True
#                         ctx['membership'].is_owner = False
#                         ctx['membership'].save()
#                 else:
#                     ctx['error_msg'] = "Invalid user id specified."

#             elif ctx['command'] == 'deleteuser':
#                 # Remove a user membership.
#                 ctx['user_id'] = int(ctx['params']['user_id']) if 'user_id' in ctx['params'] else None
#                 if ctx['user_id'] is not None:
#                     # Add a membership.
#                     ctx['membership'] = TeamMembership.objects.get(team_id=ctx['team_id'], member_id=ctx['user_id'])
#                     if ctx['membership'] is not None:
#                         ctx['membership'].delete()
#                 else:
#                     ctx['error_msg'] = "Invalid user id specified."

#             elif ctx['command'] == 'updatename':
#                 # Update the project name.
#                 ctx['team_obj'] = Project.objects.get(id=ctx['team_id'])
#                 if ctx['team_obj'] is not None:
#                     ctx['name'] = ctx['params']['name'] if 'name' in ctx['params'] else None
#                     ctx['name'] = ctx['name'].strip()
#                     if ctx['name'] is not None and ctx['name']:
#                         ctx['team_obj'].name = ctx['name']
#                         ctx['team_obj'].save()
#                     else:
#                         ctx['error_msg'] = "Invalid project name."
#                 else:
#                     ctx['error_msg'] = "Invalid project id specified."

#             # Retrieve the updated data and render the view.
#             get_request = RequestFactory().get('/')
#             get_request.user = request.user

#             ctx['team_data'] = APITeamDetailView.as_view()(
#                 get_request, team_id=ctx['team_id'], format='json').rendered_content
#             ctx['project'] = JSONParser().parse(BytesIO(ctx['team_data']))
#             ctx['nonmembers_data'] = APITeamMembershipListView.as_view()(
#                 get_request, team_id=ctx['team_id'], nonmember=1, format='json').rendered_content
#             ctx['nonmembers'] = JSONParser().parse(BytesIO(ctx['nonmembers_data']))
#             return render(request, self.template, ctx)

#         # We should never get here, so just redirect to the dashboard.
#         return HttpResponseRedirect(reverse('dashboard'))


# #########################
# # REST Api Project views
# #########################

# class APITeamListView(APIView):
#     """Get a JSON list of all projects (GET) or create a new project (POST)."""

#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, *args, **kwargs):
#         """Return all projects the current user is a member of."""
#         user = self.request.user
#         # Get the list of projects to exclude.
#         exclude = kwargs.get('exclude', None)
#         if exclude is None:
#             exclude_json = self.request.query_params.get('exclude', None)
#             if exclude_json is not None:
#                 exclude = JSONParser().parse(BytesIO(exclude_json))

#         if exclude is not None:
#             projects = (
#                 Project.objects.exclude(id__in=exclude).filter(members=user).order_by('name')
#                 .select_related("created_by", "last_modified_by")
#                 .prefetch_related("team_memberships", "team_memberships__member")
#                 .all()
#             )
#         else:
#             projects = (
#                 Project.objects.filter(members=user).order_by('name')
#                 .select_related("created_by", "last_modified_by")
#                 .prefetch_related("team_memberships", "team_memberships__member")
#                 .all()
#             )

#         serializer = TeamSerializer(projects, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         """Create a new project."""
#         serializer = TeamSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             project = serializer.save()
#             # Add a membership for the requesting user.
#             membership_instance = TeamMembership()
#             membership_instance.added_date = datetime.now()
#             membership_instance.member = request.user
#             membership_instance.project = project
#             membership_instance.is_owner = True
#             membership_instance.can_edit = True
#             membership_instance.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class APITeamDetailView(APIView):
#     """Read, Update, Delete for Project objects."""

#     permission_classes = (permissions.IsAuthenticated,)

#     @classmethod
#     def get_object(cls, p_id, user):
#         """Retrieve a project and its membership based on the provided user and p_id."""
#         try:
#             project = (
#                 Project.objects
#                 .select_related("created_by", "last_modified_by")
#                 .prefetch_related("team_memberships", "team_memberships__member")
#                 .get(id=p_id)
#             )
#             for membership in project.team_memberships.all():
#                 if user == membership.member:
#                     return project, membership
#             raise Http404
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, team_id, *args, **kwargs):
#         """Get details for the specified project."""
#         (project, _membership) = self.get_object(team_id, request.user)
#         serializer = TeamSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, team_id, *args, **kwargs):
#         """Update an existing project. :param request: :param team_id: :param format: :return:."""
#         (project, membership) = self.get_object(team_id, request.user)
#         if not membership.can_edit:
#             return Response({"detail": "current user cannot edit this project"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = TeamSerializer(project, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, team_id, *args, **kwargs):
#         """
#         Delete a project.

#         :param team_id:
#         :param request:
#         :param format:
#         :return:
#         """
#         (project, membership) = self.get_object(team_id, request.user)
#         if not membership.can_edit:
#             return Response({"detail": "current user cannot delete this project"}, status=status.HTTP_400_BAD_REQUEST)

#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class APITeamMembershipListView(APIView):
#     """Get a list of project members or users who are not project members."""

#     permission_classes = (permissions.IsAuthenticated,)

#     @classmethod
#     def get_object(cls, p_id, user):
#         """Get project memberships for the provided user and p_id."""
#         try:
#             project = (
#                 Project.objects
#                 .prefetch_related("team_memberships", "team_memberships__member")
#                 .get(id=p_id)
#             )
#             team_memberships = project.team_memberships.all()
#             for membership in team_memberships:
#                 if user == membership.member:
#                     return team_memberships
#             raise Http404
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, team_id, *args, **kwargs):
#         """Get the membership information for the specified project."""
#         # If query param "nonmember" is set, returns users not on this project.
#         nonmember = kwargs.get('nonmember', None)
#         nonmember = request.query_params.get('nonmember', None) if nonmember is None else nonmember
#         if nonmember is not None:
#             users = User.objects.exclude(member_memberships__team_id=team_id).order_by('last_name').all()
#             serializer = UserSerializer(users, many=True)
#             return Response(serializer.data)
#         team_memberships = self.get_object(team_id, request.user)
#         serializer = TeamMembershipSerializer(team_memberships, many=True)
#         return Response(serializer.data)

#     def post(self, request, team_id, *args, **kwargs):
#         """Add a new membership for a user."""
#         # Add the project info to the data.
#         request.data["project"] = team_id
#         serializer = TeamMembershipModifySerializer(data=request.data)
#         if serializer.is_valid():
#             # Make sure the membership doesn't already exist.
#             existing_membership = TeamMembership.objects.filter(team__id=team_id,
#                                                                 member__id=request.data["member"]).first()
#             if existing_membership is not None:
#                 return Response("user is already a member of this project", status=status.HTTP_400_BAD_REQUEST)
#             membership = serializer.save()
#             display_serializer = TeamMembershipSerializer(instance=membership)
#             return Response(display_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class APITeamMembershipDetailView(APIView):
#     """Get a list of project members or users who are not project members."""

#     permission_classes = (permissions.IsAuthenticated,)

#     @classmethod
#     def get_object(cls, membership_id, user):
#         """Get current membership information for the provided user and membership_id."""
#         try:
#             current_membership = (
#                 TeamMembership.objects
#                 .select_related("member", "project")
#                 .get(id=membership_id)
#             )
#             # Make sure this user can view this project information.
#             for membership in current_membership.project.team_memberships.all():
#                 if user == membership.member:
#                     return current_membership, membership.can_edit
#             raise Http404
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, team_id, membership_id, *args, **kwargs):
#         """Get details for the specified project."""
#         (membership, _current_user_can_edit) = self.get_object(membership_id, request.user)
#         serializer = TeamMembershipSerializer(instance=membership)
#         return Response(serializer.data)

#     def put(self, request, team_id, membership_id, *args, **kwargs):
#         """
#         Update an existing project.

#         :param membership_id:
#         :param request:
#         :param team_id:
#         :param format:
#         :return:
#         """
#         (membership, current_user_can_edit) = self.get_object(membership_id, request.user)
#         if not current_user_can_edit:
#             return Response({"detail": "calling user cannot edit this project"}, status=status.HTTP_400_BAD_REQUEST)

#         request.data["project"] = team_id
#         request.data["member"] = membership.member.id
#         serializer = TeamMembershipModifySerializer(membership, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, team_id, membership_id, *args, **kwargs):
#         """Delete the specified project membership."""
#         (membership, current_user_can_edit) = self.get_object(membership_id, request.user)
#         if not current_user_can_edit:
#             return Response({"detail": "calling user cannot edit this project"}, status=status.HTTP_400_BAD_REQUEST)
#         membership.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

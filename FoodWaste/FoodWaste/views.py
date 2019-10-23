# views.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of views."""

from constants.widgets import strip_non_numerals
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView
from FoodWaste.forms import TrackingToolForm
from FoodWaste.models import TrackingTool, SecondaryDataSharingTeamMap
from teams.models import TeamMembership, Team


class TrackingToolList(ListView):
    """View for Secondary / Existing Data Tracking Tool."""

    model = TrackingTool
    context_object_name = 'tracking_tool_list'
    template_name = 'trackingtool/tracking_tool_list.html'

    def get_queryset(self):
        member_teams = TeamMembership.objects.filter(member=self.request.user).values_list('team', flat=True)
        data = SecondaryDataSharingTeamMap.objects.filter(team__in=member_teams).values_list('data', flat=True)
        queryset = TrackingTool.objects.filter(id__in=data)
        return queryset



class TrackingToolCreate(CreateView):
    """Class for creating new Secondary / Existing Data."""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Secondary / Existing Data."""
        return render(request, "trackingtool/tracking_tool_create.html",
                      {'form': TrackingToolForm(user=request.user)})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Existing Data form filled out."""
        #request.POST = request.POST.copy()
        #request.POST['phone'] = '+1' + strip_non_numerals(request.POST['phone'])
        form = TrackingToolForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.disclaimer_req = form.cleaned_data['disclaimer_req']
            obj.save()
            # TODO Parse and insert attached files:
            for file in request.FILES:
                breakhere = True
            # Prepare and insert teams data
            for team_membership in form.cleaned_data['teams']:
                data_team_map = SecondaryDataSharingTeamMap()
                data_team_map.can_edit = True
                data_team_map.team = team_membership.team
                data_team_map.data = obj
                data_team_map.save()
                breakhere = True
            return HttpResponseRedirect('/trackingtool/')
        return render(request, 'trackingtool/tracking_tool_create.html',
                      {'form': form})


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'main/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'main/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

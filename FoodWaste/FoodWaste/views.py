# views.py (FoodWaste)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov


"""Definition of views."""

from constants.widgets import strip_non_numerals
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView
from FoodWaste.forms import SecondaryExistingDataForm
from FoodWaste.models import SecondaryExistingData, SecondaryDataSharingTeamMap, \
    Attachment, DataAttachmentMap
from teams.models import TeamMembership, Team


class SecondaryExistingDataList(ListView):
    """View for Secondary / Existing Data Tracking Tool."""

    model = SecondaryExistingData
    context_object_name = 'secondary_existing_data_list'
    template_name = 'secondaryexistingdata/secondary_existing_data_list.html'

    def get_queryset(self):
        # Instead of querying for member teams, filter on non-member teams and do EXCLUDE
        exclude_teams = TeamMembership.objects.exclude(member=self.request.user).values_list('team', flat=True)
        exclude_data = SecondaryDataSharingTeamMap.objects.filter(team__in=exclude_teams).values_list('data', flat=True)
        queryset = SecondaryExistingData.objects.exclude(id__in=exclude_data)
        return queryset



class SecondaryExistingDataCreate(CreateView):
    """Class for creating new Secondary / Existing Data."""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Secondary / Existing Data."""
        return render(request, "secondaryexistingdata/secondary_existing_data_create.html",
                      {'form': SecondaryExistingDataForm(user=request.user)})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Existing Data form filled out."""
        #request.POST = request.POST.copy()
        #request.POST['phone'] = '+1' + strip_non_numerals(request.POST['phone'])
        form = SecondaryExistingDataForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.disclaimer_req = form.cleaned_data['disclaimer_req']
            obj.save()
            # TODO Parse and insert attached files:
            for field in request.FILES:
                file = request.FILES[field]
                #fs = FileSystemStorage()
                #filename = fs.save(file.name, file)
                #uploaded_file_url = fs.url(filename)
                # Insert the attachment
                attch = Attachment()
                attch.uploaded_by = request.user
                attch.name = file.name
                attch.file = file
                attch.save()
                # Insert DataAttachmentMap
                attch_map = DataAttachmentMap()
                attch_map.data = obj
                attch_map.attachment = attch
                attch_map.save()
            # Prepare and insert teams data
            if form.cleaned_data['teams']:
                for team in form.cleaned_data['teams']:
                    data_team_map = SecondaryDataSharingTeamMap()
                    data_team_map.can_edit = True
                    data_team_map.team = team
                    data_team_map.data = obj
                    data_team_map.save()
            return HttpResponseRedirect('/secondaryexistingdata/')
        return render(request, 'secondaryexistingdata/secondary_existing_data_create.html',
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

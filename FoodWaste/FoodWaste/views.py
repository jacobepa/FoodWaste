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
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from FoodWaste.forms import ExistingDataForm
from FoodWaste.models import ExistingData, ExistingDataSharingTeamMap, \
    Attachment, DataAttachmentMap
from FoodWaste.settings import APP_DISCLAIMER
from teams.models import TeamMembership, Team
from wkhtmltopdf.views import PDFTemplateResponse


class ExistingDataList(ListView):
    """View for Existing Data Tracking Tool."""

    model = ExistingData
    context_object_name = 'existing_data_list'
    template_name = 'existingdata/existing_data_list.html'

    def get_queryset(self):
        # Instead of querying for member teams, filter on non-member teams and do EXCLUDE
        exclude_teams = TeamMembership.objects.exclude(member=self.request.user).values_list('team', flat=True)
        exclude_data = ExistingDataSharingTeamMap.objects.filter(team__in=exclude_teams).values_list('data', flat=True)
        queryset = ExistingData.objects.exclude(id__in=exclude_data)
        return queryset


class ExistingDataDetail(DetailView):
    """View for viewing the details of a Existing data instance"""
    model = ExistingData
    template_name = 'existingdata/existing_data_detail.html'


class ExistingDataCreate(CreateView):
    """Class for creating new Existing Data."""

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """Return a view with an empty form for creating a new Existing Data."""
        return render(request, "existingdata/existing_data_create.html",
                      {'form': ExistingDataForm(user=request.user)})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Process the post request with a new Existing Data form filled out."""
        #request.POST = request.POST.copy()
        #request.POST['phone'] = '+1' + strip_non_numerals(request.POST['phone'])
        form = ExistingDataForm(request.POST, request.FILES, user=request.user)
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
                    data_team_map = ExistingDataSharingTeamMap()
                    data_team_map.can_edit = True
                    data_team_map.team = team
                    data_team_map.data = obj
                    data_team_map.save()
            return HttpResponseRedirect('/existingdata/')
        return render(request, 'existingdata/existing_data_create.html',
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


def export_pdf(request, *args, **kwargs):
    """Function to export Existing Existing Data as a PDF document."""
    data_id = kwargs['pk']
    data = ExistingData.objects.get(id=data_id)
    filename = 'export_%s.pdf' % data.article_title
    resp = PDFTemplateResponse(
        request=request,
        template=get_template('existingdata/existing_data_detail.html'),
        filename=filename,
        context={'object': data},
        show_content_in_browser=False,
        cmd_options={},
    )
    return resp


def export_excel(request, *args, **kwargs):
    """Function to export Existing Existing Data as an Excel sheet."""
    data_id = kwargs['pk']
    data = ExistingData.objects.get(id=data_id)
    filename = 'export_%s.xlsx' % data.article_title
    from openpyxl import Workbook
    #from openpyxl.styles import PatternFill, Font
    #from openpyxl.styles.borders import Border, Side
    #from openpyxl.styles.colors import Color

    workbook = Workbook()
    sheet = workbook.active
    row = 1

    # Optionally add colors formatting before writing to cells.
    # Programmatically write results to the PDF
    for name, value in data.get_fields():
        sheet.cell(row=row, column=1).value = name
        sheet.cell(row=row, column=2).value = value
        row += 1

    if data.disclaimer_req:
        sheet.cell(row=row, column=1).value = 'Disclaimer'
        # Replace '\n                    ' with ' ' in the disclaimer
        repl_str = '\n                    '
        sheet.cell(row=row, column=2).value = APP_DISCLAIMER.replace(repl_str, ' ')

    # Now return the generated excel sheet to be downloaded.
    type = 'application/vnd.vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type=type)
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    sheet.title = filename.split('.')[0]
    workbook.save(response)
    return response

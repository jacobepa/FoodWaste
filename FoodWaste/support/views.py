# views.py (support)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov
# py-lint: disable=C0301

"""
Views for support application.

Available functions:
- View to present and process the "request more info" form.
- View to present and process the user manual view.
"""

from datetime import datetime, timedelta
from decimal import getcontext
from os.path import join
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView
from django.shortcuts import render
from FoodWaste.settings import DOWNLOADS_DIR, MANUAL_NAME
from support.forms import InformationRequestForm, SupportForm, \
    SupportAdminForm, SupportTypeForm, PriorityForm
from support.models import Support, Priority, SupportType
getcontext().prec = 9


class RequestInformationView(FormView):
    """
    View to present and process the "request more info" form.

    :param request:
    :return:
    """

    form_class = InformationRequestForm

    def get(self, request, *arg, **kwargs):
        """Present the request info form."""
        form = self.form_class()
        return render(request, 'main/request_info.html', {'form': form})

    def post(self, request, *arg, **kwargs):
        """
        Send email with information request to the website manager.

        :param request:
        :param arg:
        :param kwargs:
        :return:
        """
        form = self.form_class(request.POST)
        return render(request, 'main/request_info_done.html', {'form': form})


class UserManualView(FormView):
    """
    View to present and process the "request more info" form.

    :param request:
    :return:
    """

    form_class = InformationRequestForm

    def get(self, request, *args, **kwargs):
        """Present the request info form."""
        form = self.form_class()
        return render(request, 'main/manual.html', {'form': form})


class EventsView(TemplateView):
    """Support Upcoming Events view."""

    def get(self, request, *args, **kwargs):
        """
        :param request:.

        :param args:
        :param kwargs:
        :return:
        """
        return render(request, "main/events.html", {})

@login_required
def download_manual(request):
    """Download the user manual."""
    return download_file(request, MANUAL_NAME)


def download_file(request, name):
    """Receives the path, name, extension of a file to be returned to user."""
    name_split = name.split('.')
    ext = name_split[len(name_split) - 1]
    file = join(DOWNLOADS_DIR, name)

    if ext == 'pdf':
        with open(file, 'rb') as pdf:
            response = HttpResponse(pdf)
            con_disp = 'attachment; filename="' + name + '"'
            response['Content-Disposition'] = con_disp
            return response

    elif ext == 'docx':
        with open(file, 'rb') as doc:
            response = HttpResponse(doc)
            con_disp = 'attachment; filename="' + name + '"'
            response['Content-Disposition'] = con_disp
            return response

    elif 'xls' in ext:
        with open(file, 'rb') as xls:
            con_type = '''application/vnd.vnd.openxmlformats-officedocument.
                          spreadsheetml.sheet'''
            response = HttpResponse(xls, con_type)
            con_disp = 'attachment; filename="' + name + '"'
            response['Content-Disposition'] = con_disp
            return response

    return HttpResponse()

@login_required
def index(request):
    """Returns the main support page view."""
    user = request.user
    title = "Support Main Page"
    objs = Support.objects.filter(user=user)
    return render(request, 'main/support.html',
                  {'user': user, 'title': title, 'objs': objs})


@login_required
def create_support(request):
    """
    This method handles GET and POST requests to either give the user a
    blank support form, or to process a completed support form from the user.
    """
    ctx = {'user': request.user, 'title': "Create a New Support Issue",
           'supports': Support.objects.all()}

    if request.method == "POST":
        ctx['form'] = SupportForm(data=request.POST, files=request.FILES)
        if ctx['form'].is_valid():
            if 'files' in request.FILES:
                ctx['files'] = request.FILES['files']
                ctx['files'].user = ctx['user']

            ctx['support'] = ctx['form'].save(commit=False)

            ctx['support'].user = ctx['user']
            ctx['support'].created_by = ctx['user'].username
            ctx['support'].last_modified_by = ctx['user'].username
            ctx['support'].save()
            send_mail(
                'Food Waste Support Request',
                '''A Food Waste Support Request Has Been Submitted
                . Here is the description of the issue: %s'''
                % str(ctx['support'].the_description),
                ctx['support'].weblink,
                ['young.daniel@epa.gov'],
                fail_silently=False)
            url = '/support/show/%s/' % str(ctx['support'].id)
            return HttpResponseRedirect(url)
    else:
        ctx['form'] = SupportForm()
    return render(request, 'create/create.html', ctx)


@login_required
def edit_support(request, obj_id):
    """
    This method retrieves existing Support requests to allow a user
    to make modifications to the request.
    """
    ctx = {'user': request.user, 'title': "Update Support",
           'support': Support.objects.get(id=obj_id)}

    if ctx['user'].is_staff:
        url = '/support/edit/admin/%s/' % str(ctx['support'].id)
        return HttpResponseRedirect(url)
    if ctx['user'] != ctx['support'].user:
        return render(request, 'no_edit.html', ctx)

    if ctx['support'].user == ctx['user']:
        if request.method == "POST":
            ctx['form'] = SupportForm(data=request.POST,
                                      files=request.FILES,
                                      instance=ctx['support'])
            if ctx['form'].is_valid():
                ctx['support'] = ctx['form'].save(commit=False)
                ctx['support'].last_modified_by = ctx['user'].username
                ctx['support'].save()
                url = '/support/show/%s/' % str(ctx['support'].id)
                return HttpResponseRedirect(url)
        else:
            ctx['form'] = SupportForm(instance=ctx['support'])
    else:
        ctx['url'] = '/accounts/not_authorized/'

    return render(request, 'edit/edit.html', ctx)


@login_required
def edit_support_admin(request, obj_id):
    """
    This method retrieves existing Support requests to allow an
    admin user to make modifications to the request.
    """
    ctx = {'user': request.user, 'title': "Update Support",
           'support': Support.objects.get(id=obj_id)}

    if ctx['user'].is_staff:
        pass
    else:
        return render(request, 'no_edit.html', ctx)

    if ctx['support'].user == ctx['user']:
        if request.method == "POST":
            ctx['form'] = SupportAdminForm(data=request.POST,
                                           files=request.FILES,
                                           instance=ctx['support'])
            if ctx['form'].is_valid():
                ctx['support'] = ctx['form'].save(commit=False)

                ctx['support'].last_modified_by = ctx['user'].username
                ctx['support'].save()

                url = '/support/show/%s/' % str(ctx['support'].id)
                return HttpResponseRedirect(url)
        else:
            ctx['form'] = SupportAdminForm(instance=ctx['support'])
    else:
        ctx['url'] = '/accounts/not_authorized/'

    return render(request, 'edit.html', ctx)


@login_required
def delete_support(request, obj_id):
    """This method deletes the provided support request from the database."""
    user = request.user
    support = get_object_or_404(Support, id=obj_id)
    if support.user == user or user.is_staff:
        support.delete()

    url = '/support/list/'
    return HttpResponseRedirect(url)


@login_required
def list_supports(request):
    """This method returns a list of support requests from the database."""
    user = request.user
    title = "Support List"
    supports = Support.objects.filter(is_closed="N")
    return render(request, 'list/list_support_issues.html',
                  {'user': user, 'title': title, 'supports': supports})


@login_required
@never_cache
def show_support(request, obj_id):
    """This method is used to view details of a given support request."""
    user = request.user
    obj = get_object_or_404(Support, id=obj_id)
    title = "Show Support"
    return render(request, 'show/show_support.html',
                  {'user': user, 'obj': obj, 'title': title})


def search_support(request):
    """This method directs the user to the support search page."""
    title = "Search For Support - With Results Shown"
    return render(request, 'list/list_support_issues.html', {'title': title})


@login_required
def search_support_for_last_30(request):
    """
    This method performs a search for the provided query,
    filtering on the previous 30 days.
    """
    ctx = {
        'user': request.user, 'query': Q(),
        'query_show': 'Support Requests Received For Last 30 Days',
        'title': "Support Requests Received Last 30 Days - With Results Shown",
        'date': datetime.today() - timedelta(days=30)}
    if ctx['user'].is_staff:
        ctx['query'] = Q(created__gte=ctx['date'])
    else:
        ctx['query'] = Q(created__gte=ctx['date']) & Q(user=ctx['user'])

    if ctx['query']:
        ctx['the_count'] = Support.objects.filter(ctx['query']).count()
        ctx['objs'] = Support.objects.filter(ctx['query'])
    else:
        ctx['objs'] = ""

    return render(request, 'list/list_support_issues.html', ctx)


@login_required
def search_support_for_last_60(request):
    """
    This method performs a search for the provided query,
    filtering on the previous 60 days.
    """
    ctx = {
        'user': request.user, 'query': Q(),
        'query_show': 'Support Requests Received For Last 60 Days',
        'title': "Support Requests Received Last 60 Days - With Results Shown",
        'date': datetime.today() - timedelta(days=60)}
    if ctx['user'].is_staff:
        ctx['query'] = Q(created__gte=ctx['date'])
    else:
        ctx['query'] = Q(created__gte=ctx['date']) & Q(user=ctx['user'])

    if ctx['query']:
        ctx['the_count'] = Support.objects.filter(ctx['query']).count()
        ctx['objs'] = Support.objects.filter(ctx['query'])
    else:
        ctx['objs'] = ""

    return render(request, 'list/list_support_issues.html', ctx)


@login_required
def search_support_for_last_90(request):
    """
    This method performs a search for the provided query,
    filtering on the previous 90 days.
    """
    ctx = {
        'user': request.user, 'query': Q(),
        'query_show': 'Support Requests Received For Last 90 Days',
        'title': "Support Requests Received Last 90 Days - With Results Shown",
        'date': datetime.today() - timedelta(days=90)}
    if ctx['user'].is_staff:
        ctx['query'] = Q(created__gte=ctx['date'])
    else:
        ctx['query'] = Q(created__gte=ctx['date']) & Q(user=ctx['user'])

    if ctx['query']:
        ctx['the_count'] = Support.objects.filter(ctx['query']).count()
        ctx['objs'] = Support.objects.filter(ctx['query'])
    else:
        ctx['objs'] = ""

    return render(request, 'list/list_support_issues.html', ctx)


@login_required
def search_support_for_last_180(request):
    """
    This method performs a search for the provided query,
    filtering on the previous 180 days.
    """
    ctx = {
        'user': request.user, 'query': Q(),
        'query_show': 'Support Requests Received For Last 180 Days',
        'title':'Support Requests Received Last 180 Days - With Results Shown',
        'date': datetime.today() - timedelta(days=180)}
    if ctx['user'].is_staff:
        ctx['query'] = Q(created__gte=ctx['date'])
    else:
        ctx['query'] = Q(created__gte=ctx['date']) & Q(user=ctx['user'])

    if ctx['query']:
        ctx['the_count'] = Support.objects.filter(ctx['query']).count()
        ctx['objs'] = Support.objects.filter(ctx['query'])
    else:
        ctx['objs'] = ""

    return render(request, 'list/list_support_issues.html', ctx)


@login_required
def create_support_type(request):
    """
    This method handles GET and POST requests to either give the user a
    blank form to create a new Support Type, or receives a completed form
    to create a new Support Type.
    """
    ctx = {'user': request.user, 'title': "Create a New SupportType",
           'support_types': SupportType.objects.all()}

    if request.method == "POST":
        ctx['form'] = SupportTypeForm(data=request.POST, files=request.FILES)
        if ctx['form'].is_valid():
            if 'files' in request.FILES:
                ctx['files'] = request.FILES['files']
                ctx['files'].user = ctx['user']

            ctx['support_type'] = ctx['form'].save(commit=False)

            ctx['support_type'].user = ctx['user']
            ctx['support_type'].created_by = ctx['user'].username
            ctx['support_type'].last_modified_by = ctx['user'].username
            ctx['support_type'].save()

            url = '/support/type/show/%s/' % str(ctx['support_type'].id)
            return HttpResponseRedirect(url)
    else:
        ctx['form'] = SupportTypeForm()
    return render(request, 'create/create.html', ctx)


@login_required
def edit_support_type(request, obj_id):
    """
    This method retrieves existing Support types to allow a
    user to make modifications to it.
    """
    ctx = {'user': request.user, 'title': "Update SupportType",
           'support_type': SupportType.objects.get(id=obj_id),
           'support_types': SupportType.objects.all()}
    if ctx['user'].is_staff or ctx['user'] == ctx['support_type'].user:
        pass
    else:
        return render(request, 'no_edit.html', ctx)

    if ctx['support_type'].user == ctx['user']:
        if request.method == "POST":
            ctx['form'] = SupportTypeForm(data=request.POST,
                                          files=request.FILES,
                                          instance=ctx['support_type'])
            if ctx['form'].is_valid():
                ctx['support_type'] = ctx['form'].save(commit=False)
                ctx['support_type'].last_modified_by = ctx['user'].username
                ctx['support_type'].save()
                url = '/support/type/show/%s/' % str(ctx['support_type'].id)
                return HttpResponseRedirect(url)
        else:
            ctx['form'] = SupportTypeForm(instance=ctx['support_type'])
    else:
        ctx['url'] = '/accounts/not_authorized/'

    return render(request, 'edit/edit.html', ctx)


@login_required
def delete_support_type(request, obj_id):
    """This method deletees a Support Type from the database."""
    user = request.user
    support_type = get_object_or_404(SupportType, id=obj_id)

    if support_type.user == user:
        support_type.delete()

    url = '/support/type/list/'
    return HttpResponseRedirect(url)


@login_required
def list_support_types(request):
    """This method returns a list of support types to be displayed."""
    ctx = {'user': request.user, 'title': "SupportType List",
           'support_types': SupportType.objects.all().order_by('ordering')}
    return render(request, 'list/list_support_types.html', ctx)


@login_required
@never_cache
def show_support_type(request, obj_id):
    """This method returns a single support type to display its details."""
    ctx = {'user': request.user,
           'obj': get_object_or_404(SupportType, id=obj_id),
           'title': "Show SupportType",
           'support_types': SupportType.objects.all().order_by('ordering')}
    return render(request, 'show/show.html', ctx)


def search_support_type(request):
    """
    This method returns the view that will allow users to search support types.
    """
    title = "Search For SupportType - With Results Shown"
    return render(request, 'main/search_support_type.html', {'title': title})


@login_required
def create_priority(request):
    """
    This method handles GET and POST requests to either give the user a
    blank form to create a new Priority, or receives a completed form
    to create a new Priority.
    """
    ctx = {'user': request.user, 'title': "Create a New Priority",
           'priorities': Priority.objects.all()}

    if request.method == "POST":
        ctx['form'] = PriorityForm(data=request.POST, files=request.FILES)
        if ctx['form'].is_valid():
            if 'files' in request.FILES:
                ctx['files'] = request.FILES['files']
                ctx['files'].user = ctx['user']

            ctx['priority'] = ctx['form'].save(commit=False)

            ctx['priority'].user = ctx['user']
            ctx['priority'].created_by = ctx['user'].username
            ctx['priority'].last_modified_by = ctx['user'].username
            ctx['priority'].save()

            url = '/support/priority/show/%s/' % str(ctx['priority'].id)
            return HttpResponseRedirect(url)
    else:
        ctx['form'] = PriorityForm()
    return render(request, 'create_office.html', ctx)


@login_required
def edit_priority(request, obj_id):
    """This method allows the user to edit an existing Priority."""
    ctx = {'user': request.user, 'title': "Update Priority",
           'priority': Priority.objects.get(id=obj_id),
           'priorities': Priority.objects.all()}

    if ctx['user'].is_staff or ctx['user'] == ctx['priority'].user:
        pass
    else:
        return render(request, 'no_edit.html', ctx)

    if ctx['priority'].user == ctx['user']:
        if request.method == "POST":
            ctx['form'] = PriorityForm(data=request.POST,
                                       files=request.FILES,
                                       instance=ctx['priority'])
            if ctx['form'].is_valid():
                ctx['priority'] = ctx['form'].save(commit=False)

                ctx['priority'].last_modified_by = ctx['user'].username
                ctx['priority'].save()

                url = '/support/priority/show/%s/' % str(ctx['priority'].id)
                return HttpResponseRedirect(url)
        else:
            ctx['form'] = PriorityForm(instance=ctx['priority'])
    else:
        ctx['url'] = '/accounts/not_authorized/'

    return render(request, 'edit_office.html', ctx)


@login_required
def delete_priority(request, obj_id):
    """This method deletes a Priority from the database."""
    user = request.user
    priority = get_object_or_404(Priority, id=obj_id)
    if priority.user == user:
        priority.delete()

    url = '/support/priority/list/'
    return HttpResponseRedirect(url)


@login_required
def list_priorities(request):
    """This method returns a list of priorities to a view."""
    user = request.user
    title = "Priority List"
    priorities = Priority.objects.all().order_by('ordering')
    return render(request, 'list/list_priorities.html',
                  {'user': user, 'title': title, 'priorities': priorities})


@login_required
@never_cache
def show_priority(request, obj_id):
    """This method returns a single priority to view its details."""
    user = request.user
    obj = get_object_or_404(Priority, id=obj_id)
    title = "Show Priority"
    return render(request, 'show/show.html', {'user': user, 'obj': obj,
                                              'title': title})


def search_priority(request):
    """This method directs to the page where priorities can be searched."""
    title = "Search For Priority - With Results Shown"
    return render(request, 'main/search_priority.html', {'title': title})

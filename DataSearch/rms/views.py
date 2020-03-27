from django.shortcuts import render

from rms.models import *

from django.shortcuts import render, get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache, cache_control
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
import json
#from django.apps import get_model
from django.db.models import Q
from constants.perms import apply_perms


# Create your views here.
@login_required
@apply_perms
def index(request, **kwargs):
    user = request.user

    # get the program data
    programs = Program.objects.order_by('acronym').all()
    program_list = json.dumps([{"id": obj.id, "acronym": obj.acronym, "title": obj.title}
                               for obj in programs])

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    programs = Program.objects.all().order_by('acronym')

    return render(request, 'main/rms_projects.html', locals())

@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@apply_perms
def show_project(request, project_id, **kwargs):
    print(project_id)
    user = request.user
    profile = user.userprofile
    obj = get_object_or_404(Project, id=project_id)
    title = "Show Project"

    project_attachments = RMSProjectAttachment.objects.filter(project=obj)
    return render(request, 'show/show_rms_project.html', locals())

@login_required
@apply_perms
def file_upload(request, obj_id, **kwargs):
    user = request.user
    project = Project.objects.get(id=obj_id)
    print(obj_id)

    # Loop through our files in the files list uploaded
    for new_file in request.FILES.getlist('upl'):
        # print("Found a file " + new_file.name)
        try:
            project_attachment, created = RMSProjectAttachment.objects.get_or_create(project=project, attachment=new_file, file_name=new_file.name, created_by_user=user, file_size=new_file.size)
        except Exception as e:
            print(e)
        # print("created = " #+ created)

    url = '/rms/show/%s/' % str(project.id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def search_project(request, **kwargs):
    user = request.user

    # get the program data
    programs = Program.objects.order_by('acronym').all()
    program_list = json.dumps([{"id": obj.id, "acronym": obj.acronym, "title": obj.title}
                           for obj in programs])

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    programs = Program.objects.all().order_by('acronym')

    return render(request, 'main/search_rms_projects.html', locals())

@login_required
@apply_perms
def result_search_project(request, **kwargs):
    user = request.user

    query = Q()
    query_show = ''

    program_id = request.GET.get("program", None)

    if program_id is not None and program_id != '':
        program = Program.objects.get(id = program_id)
        query = query & (Q(program__id=program_id))
        query_show = query_show + "ORD RAP Program = " + str(program.acronym) + " "

    if 'epa_id' in request.GET:
        epa_id = request.GET['epa_id']
        if epa_id:
            query = query & (Q(epa_id__icontains=epa_id))
            query_show = query_show + "EPA ID => " + str(epa_id) + " "

    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            query = query & (Q(title__icontains=title))
            query_show = query_show + "Title => " + str(title) + " "

    if 'has_attachments' in request.GET:
        has_attachments = request.GET['has_attachments']
        if has_attachments != '':
            if has_attachments == 'Y':
                no_attachments = False
            if has_attachments == 'N':
                no_attachments = True

            # print(no_attachments)
            query = query & (Q(rmsprojectattachment__isnull=no_attachments))
            query_show = query_show + "Has ORD QA Planning Form(s) => " + str(has_attachments)

    projects = Project.objects.filter(query).all()
    the_count = len(projects)
    query_show = query_show

    return render(request, 'main/search_rms_project_result.html', locals())


@login_required
@apply_perms
def delete_project_attachment(request, obj_id, **kwargs):
    title = "Delete Project Attachment"
    user = request.user
    project_attachment = get_object_or_404(RMSProjectAttachment, id=obj_id)
    project = project_attachment.project

#    if project_attachment.created_by_user == user or user.is_staff:
    if project_attachment.created_by_user == user or kwargs["is_admin"]:
        project_attachment.delete()

    url = '/rms/show/%s/' % str(project.id)
    return HttpResponseRedirect(url)

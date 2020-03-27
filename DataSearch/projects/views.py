from django.shortcuts import render
import xlwt
import csv
import datetime
from datetime import datetime, timedelta
from . import models
import os
import re
import json
import profile
import urllib.parse
from operator import itemgetter

# Added to handle exporting to Excel
import io
import xlsxwriter

from math import *
from decimal import *
getcontext().prec = 9
from time import gmtime, strftime, localtime

from accounts.models import *

from constants.models import *
from constants.utils import *

from projects.models import *
from projects.forms import *

from support.models import *
from organization.models import *

from django.forms.models import modelformset_factory, inlineformset_factory

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission

from django.conf import settings

from django.core import serializers
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from django.forms.models import modelformset_factory, inlineformset_factory

#from django.apps import get_model
from django.db.models import Q, Avg, Max, Min, Count, Sum


from django.http import Http404, HttpResponseRedirect, HttpResponse

from django.shortcuts import render, get_object_or_404

from django.template import RequestContext, loader, Context

from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.colors import pink, black, red, blue, green, lightgrey, ghostwhite, whitesmoke
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, flowables, SimpleDocTemplate, Image, Spacer
from reportlab.platypus.flowables import Flowable
from django.views.generic import FormView, TemplateView
from reportlab.rl_config import defaultPageSize
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]
from io import BytesIO
import organization.query_utils as oq
from django.core import serializers

from sop_tab.models import *
from notebooks_tab.models import *

from django.shortcuts import render, redirect

from constants.perms import apply_perms
from django.utils import timezone


class flowable_rect(Flowable):
    def __init__(self, width, height, checked=False):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.checked = checked

    def draw(self):
        if self.checked==False:
            self.canv.rect(0, -3, self.width, self.height, fill=0)
        else:
            self.canv.rect(0, -3, self.width, self.height, fill=1)


# rect = flowable_rect(6, 6)
# t_opt_1=Table([[rect,option_1]], style=style_table,
#              colWidths=[100, 200], hAlign="LEFT")


def get_file_type(filename):
    valid_doc_extensions = ['doc', 'docx', 'docm']
    valid_pdf_extensions = ['pdf']
    extension = filename.split('.').pop().lower()
    if extension in valid_doc_extensions:
        return 'doc'
    elif extension in valid_pdf_extensions:
        return 'pdf'
    else:
        return None

def get_latest_ep(queryset):
    if queryset.count() == 0:
        return None

    current_ep = queryset.first()

    for ep in queryset:
        if ep.qa_log_number_x > current_ep.qa_log_number_x:
            current_ep = ep
        elif ep.qa_log_number_x == current_ep.qa_log_number_x:
            if ep.qa_log_number_y > current_ep.qa_log_number_y:
                current_ep = ep
    return current_ep

def get_project_users(project=None,qlog=None):
    project_users = []
    #either pass qlog or project
    if project is None:
        project = Project.objects.filter(pk=qlog.project_id).first()

    qlogs = ProjectLog.objects.filter(project=project)
    #project people
    project_users.append(project.user)
    project_users.append(project.person)
    for u in project.collaborators.all():
        project_users.append(u)

    for log in qlogs:
        project_users.append(log.user)
        project_users.append(log.reviewer)
        project_users.append(log.technical_lead)

    return list(set(project_users))


class ActivitySummaryByUserView(TemplateView):
    """
    View a summary of activities for the specified user
    """

    template_name = "main/activity_summary_user.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Display a summary
        """
        user_id = kwargs['user_id']
        selected_user = User.objects.get(id = user_id)

        projects = Project.objects.filter(person=selected_user)
        reviews = ProjectLog.objects.filter(reviewer=selected_user)
        qlogs = ProjectLog.objects.filter(technical_lead=selected_user)
        return render(request, self.template_name, locals())


class ProjectCreateView(FormView):
    """
    View to create a new project.  Allows the user to specify the
    office/lab/division with which the project is associated, and then

    """
    form_class = ProjectFormAsync
    template_start = "main/create_project_start.html"
    template_create = "main/create_project.html"

    rap_fields = get_rap_fields();


    def _setup_organization_select(self, user):
        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

        # formatting for the organization selector
        office_required = True
        lab_required = True
        division_required = True
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        return (office_list, lab_list, division_list, branch_list,
                office_required, lab_required, division_required, label_class, input_container_class)


    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Start a new project
        """
        user = request.user

        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(user)
        selected_office = user.userprofile.office
        selected_lab = user.userprofile.lab
        selected_division = user.userprofile.division
        selected_branch = user.userprofile.branch

        return render(request, self.template_start, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        """
        Create the project
        """
        user = request.user
        (office_list, lab_list, division_list,
         branch_list, office_required, lab_required, division_required,
         label_class, input_container_class) = self._setup_organization_select(user)
        label_class = "col-sm-4"
        input_container_class = "col-sm-8"

        post_params = request.POST.copy()
        date_now = timezone.now()
        post_params["created"] = date_now
        post_params["created_by"] = user.username
        post_params["modified"] = date_now
        post_params["last_modified_by"] = user.username

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)
        form = self.form_class(data=post_params, is_editable=True, is_new=True, office_id=office_id, lab_id=lab_id, division_id=division_id, branch_id=branch_id)

        rap_fields = get_rap_fields()
        rap_numbers = get_rap_numbers()

        if "create_finish" in request.POST:
            if form.is_valid():
                project_number = ProjectNumber.objects.get(id=1)
                this_serial_number_str = str(project_number.this_serial_number).zfill(7)

                project = form.save(commit=False)

                if project.date_project_identified == '':
                    project.date_project_identified = None
                if project.qapp_approval_date == '':
                    project.qapp_approval_date = None
                if project.qmp_approval_date == '':
                    project.qmp_approval_date = None
                if project.last_qapp_review_date == '':
                    project.last_qapp_review_date = None


                for rap in rap_fields:
                    setattr(project,rap,getattr(project,rap).strip(',;'))

                project.user = user
                project.created_by = user.username
                project.last_modified_by = user.username
                project.qa_id = project.lab.designation_code + "-" + project.division.abbreviation.split()[0] + "-" + \
                                this_serial_number_str
                project_number.this_serial_number += 1
                project_number.save()
                project.save()
                form.save_m2m()

                # add to update history
                project_update_history = Project_update_history.objects.create(project=project,
                                                                                      user=user,
                                                                                      date_qappreviewed=project.last_qapp_review_date,
                                                                                      projectlead=project.person,
                                                                                      qa_manager=project.qa_manager,
                                                                                      project_status=project.project_status,
                                                                                      qapp_status=project.qapp_status,
                                                                                      comments='Project created')

                return HttpResponseRedirect(reverse('show_project', kwargs={"project_id": project.id}))
            else:

                selected_office = Office.objects.get(id = office_id) if oq._valid_org_id(office_id) else None
                selected_lab = Lab.objects.get(id = lab_id) if oq._valid_org_id(lab_id) else None
                selected_division = Division.objects.get(id = division_id) if oq._valid_org_id(division_id) else None
                selected_branch = Branch.objects.get(id = branch_id) if oq._valid_org_id(branch_id) else None

                return render(request, self.template_create, locals())

        else:
            office_id = request.POST.get("office", None)
            lab_id = request.POST.get("lab", None)
            division_id = request.POST.get("division", None)
            branch_id = request.POST.get("branch", None)
            show_inactive_orgs = request.POST.get("show_inactive_orgs", None)
            ## we get here when the user submits from the create start page
            selected_office = Office.objects.get(id = office_id) if oq._valid_org_id(office_id) else user.userprofile.office
            selected_lab = Lab.objects.get(id = lab_id) if oq._valid_org_id(lab_id) else user.userprofile.lab
            selected_division = Division.objects.get(id = division_id) if oq._valid_org_id(division_id) else user.userprofile.division
            selected_branch = Branch.objects.get(id = branch_id) if oq._valid_org_id(branch_id) else None
            active_status = ProjectStatus.objects.filter(the_name = 'Active').first()

            if oq._valid_org_id(office_id) and oq._valid_org_id(lab_id) and oq._valid_org_id(division_id):
                # Passing in org info so the project QA Manager field can be initialized to org's QA manager
                form = ProjectFormAsync(initial={"project_status": active_status}, is_editable=True, is_new=True, office_id=office_id, lab_id=lab_id, division_id=division_id, branch_id=branch_id)

                # fill in the rest of the details for the project
                return render(request, self.template_create, locals())

            else:
                error = "Please select an office, a lab, and a division for this project"
                return render(request, self.template_start, locals())


class ProjectUpdateView(FormView):
    """
    View to edit a project.

    """
    form_class = ProjectFormAsync
    template_name = "main/edit_project.html"


    def _setup_organization_select(self, user):
        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

        # formatting for the organization selector
        office_required = True
        lab_required = True
        division_required = True
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        return (office_list, lab_list, division_list, branch_list,
                office_required, lab_required, division_required, label_class, input_container_class)

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, *args, **kwargs):
        """
        Display a summary
        """
        user = request.user
        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(user)
        project_id = kwargs["project_id"]
        obj = Project.objects.get(id = project_id)
        selected_office = obj.office
        selected_lab = obj.lab
        if selected_lab:
            lab_id = selected_lab.id
        else:
            lab_id = 0
        selected_division = obj.division
        if selected_division:
            division_id = selected_division.id
        else:
            division_id = 0
        selected_branch = obj.branch
        if selected_branch:
            branch_id = selected_branch.id
        else:
            branch_id = 0
        form = self.form_class(instance=obj, is_editable=True, is_new=False, office_id=selected_office.id, lab_id=lab_id, division_id=division_id, branch_id=branch_id)

        rap_fields = get_rap_fields()
        rap_numbers = get_rap_numbers()
        label_width = 3 #for use in edit_project_rap_group.html
        field_width = 9

        project_update_history = Project_update_history.objects.filter(project=obj)

        return render(request, self.template_name, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, *args, **kwargs):
        user = request.user
        (office_list, lab_list, division_list, branch_list, office_required,
         lab_required, division_required, label_class, input_container_class) = self._setup_organization_select(user)
        project_id = kwargs["project_id"]
        obj = Project.objects.get(id = project_id)
#        selected_office = obj.office
#        selected_lab = obj.lab
#        selected_division = obj.division
#        selected_branch = obj.branch

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        rap_fields = get_rap_fields()
        label_width = 3 #for use in edit_project_rap_group.html
        field_width = 9

        form = self.form_class(data=request.POST, files=request.FILES, instance=obj, is_editable=True, is_new=False, office_id=office_id, lab_id=lab_id, division_id=division_id, branch_id=branch_id)

        before_last_qapp_review_date = obj.last_qapp_review_date
        before_projectlead = obj.person
        before_qa_manager = obj.qa_manager
        before_project_status = obj.project_status
        before_qapp_status = obj.qapp_status
        update_comments = request.POST.get("update_comment")

        if form.is_valid():
            project = form.save(commit=False)
            if project.date_project_identified == '':
                project.date_project_identified = None
            if project.qapp_approval_date == '':
                project.qapp_approval_date = None
            if project.qmp_approval_date == '':
                project.qmp_approval_date = None
            if project.last_qapp_review_date == '':
                project.last_qapp_review_date = None

            for rap in rap_fields:
                setattr(project,rap,getattr(project,rap).strip(',;'))

            project.last_modified_by = user.username
            project.modified = timezone.now()
            project.save()
            form.save_m2m()

            log_hist = False
            if before_last_qapp_review_date != project.last_qapp_review_date:
                log_hist = True
            elif before_projectlead != project.person:
                log_hist = True
            elif before_qa_manager != project.qa_manager:
                log_hist = True
            elif before_project_status != project.project_status:
                log_hist = True
            elif before_qapp_status != project.qapp_status:
                log_hist = True
            elif update_comments:
                log_hist = True

            if log_hist:
                # add to update history
                project_update_history = Project_update_history.objects.create(project=project,
                                                                               user=user,
                                                                               date_qappreviewed=project.last_qapp_review_date,
                                                                               projectlead=project.person,
                                                                               qa_manager=project.qa_manager,
                                                                               project_status=project.project_status,
                                                                               qapp_status=project.qapp_status,
                                                                               comments=update_comments)

            url = '/projects/show/%s/' % str(project.id)
            return HttpResponseRedirect(url)
        else:

            selected_office = Office.objects.get(id=office_id) if oq._valid_org_id(office_id) else None
            selected_lab = Lab.objects.get(id=lab_id) if oq._valid_org_id(lab_id) else None
            selected_division = Division.objects.get(id=division_id) if oq._valid_org_id(division_id) else None
            selected_branch = Branch.objects.get(id=branch_id) if oq._valid_org_id(branch_id) else None

            return render(request, self.template_name, locals())


@login_required
@apply_perms
def index(request,**kwargs):
    user = request.user
    title = "Projects Main Page"

    return render(request, 'main/projects.html', locals())

@login_required
@apply_perms
def go_to_qlogs(request,**kwargs):
    user = request.user
    title = "QA Activities Main Page"
    return render(request, 'main/project_logs.html', locals())



@login_required
@apply_perms
def go_to_qapp_review(request,**kwargs):
    user = request.user
    title = "Annual QAPP Reviews Main Page"

    # # get the email text
    html_file = os.path.join(os.path.dirname(__file__), 'templates/qappReview.txt')
    f = open(html_file, 'r')

    return render(request, 'main/qapp_review.html', locals())

@login_required
@apply_perms
def go_to_reviews(request,**kwargs):
    user = request.user
    title = "QA Review Main Page"
    return render(request, 'main/reviews.html', locals())

@login_required
@apply_perms
def file_upload(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile
    project = Project.objects.get(id=obj_id)

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/projects/list/lab/project/"
#        return render(request, 'error.html', locals())


    # Loop through our files in the files list uploaded
    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        project_attachment, created = ProjectAttachment.objects.get_or_create(project=project, attachment=new_file, the_name=new_file.name, user=user, the_size=new_file.size, where_from="Project")

    url = '/projects/show_expanded/%s/#attachments' % str(project.id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def file_upload_project_log(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile
    project_log = ProjectLog.objects.get(id=obj_id)
    project = project_log.project

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/projects/list/lab/project/"
#        return render(request, 'error.html', locals())

    # Loop through our files in the files list uploaded
    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        project_attachment, created = ProjectAttachment.objects.get_or_create(project=project, project_log=project_log, attachment=new_file, the_name=new_file.name, user=user, the_size=new_file.size, where_from="QA Activity")

    url = '/projects/qlog/show_expanded/%s/#attachments' % str(project_log.id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def file_upload_qa_review(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile
    project_log = ProjectLog.objects.get(id=obj_id)
    project = project_log.project

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/projects/list/lab/project/"
#        return render(request, 'error.html', locals())

    # Loop through our files in the files list uploaded
    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        project_attachment, created = ProjectAttachment.objects.get_or_create(project=project, project_log=project_log, attachment=new_file, the_name=new_file.name, user=user, the_size=new_file.size, where_from="QA Review")

    url = '/projects/qa_review/show/%s/' % str(project_log.id)
    return HttpResponseRedirect(url)



# obj_id - id of project to toggle flag for
# qapp_annual_SQL - SQL query to recreate search
# query_show - description of query to display again on refresh
@login_required
@apply_perms
def switch_qapp_reminder_flag(request, obj_id, **kwargs):

    user = request.user
    project = get_object_or_404(Project, id=obj_id)

    if project.suspend_reminder != "Y":
        project.suspend_reminder = "Y"
    else:
        project.suspend_reminder = "N"

    project.save()

    referer_url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(referer_url)



@login_required
@apply_perms
def search_qapp_annual_review(request,**kwargs):
    user = request.user
    title = "Search SOPs"

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    # selected_branch = user.userprofile.branch

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    return render(request, 'main/search_qapp_annual_review.html', locals())

@login_required
@apply_perms
def result_search_qapp_annual_review(request,**kwargs):

    #global qapp_annual_SQL
    #global qapp_annual_criteria

    the_count = 0
    user = request.user
    lead_office_id = request.GET.get("office", None)

    if lead_office_id is not None:
        #NOTE: If you change qapp_annual_SQL, the metrics tab qapp needs review column may also need to change.
        qapp_annual_SQL = (
            "select p.id, p.qa_id, p.title, p.qapp_approval_date, u1.email as project_lead, u2.email as qapp_reviewer, u3.email as qa_manager,  "
            "p.office_id as office_id, "
            "p.lab_id as lab_id, "
            "p.division_id as division_id, "
            "p.branch_id as branch_id, "
            "qr.last_email_sent, p.last_qapp_review_date, p.suspend_reminder, "
            "COALESCE(p.last_qapp_review_date, p.qapp_approval_date) as qapp_date, "
            "(select abbreviation from organization_office where id = p.office_id) as office, "
            "(select abbreviation from organization_lab where id = p.lab_id) as lab, "
            "(select abbreviation from organization_division where id = p.division_id) as division, "
            "(select abbreviation from organization_branch where id = p.branch_id) as branch from "
            "(select project_id, max(reviewer_id) as reviewer_id from "
            "(select pl.project_id, date_approved, reviewer_id from projects_projectlog pl "
            "inner join "
            "(select project_id, max(date_approved) as latest_date from projects_projectlog "
            "where project_log_type_id = (select id from projects_projectlogtype where the_name = 'QAPP') "
            "group by project_id) latest_pl "
            "on (latest_pl.project_id = pl.project_id and latest_pl.latest_date = pl.date_approved) "
            "inner join projects_projectlogtype plt on (pl.project_log_type_id = plt.id) "
            "where plt.the_name = 'QAPP') pl_info "
            "group by project_id, date_approved) pl "
            "inner join projects_project p on (pl.project_id = p.id) "
            "left join auth_user u1 on (u1.id = p.person_id) "
            "left join auth_user u2 on (u2.id = pl.reviewer_id) "
            "left join auth_user u3 on (u3.id = p.qa_manager_id) "
            "left join (select project_id, max(date_email_sent) as last_email_sent from projects_qappReview "
            "group by project_id) qr on (qr.project_id = p.id) "
            "where COALESCE(p.last_qapp_review_date, p.qapp_approval_date) < (now() - INTERVAL '1 year') "
            "and p.project_status_id = (select id from projects_projectstatus where the_name = 'Active') "
            "and p.qapp_status_id = (select id from projects_qappstatus where the_name = 'QAPP Approved') "
        )

        # return HttpResponse(qapp_annual_SQL)

        lead_lab_id = request.GET.get("lab", None)
        lead_division_id = request.GET.get("division", None)
        lead_branch_id = request.GET.get("branch", None)

        ## Add criteria to baseSQL
        qapp_annual_criteria = ''
        if lead_office_id is not None and lead_office_id != '':
            qapp_annual_SQL += " and office_id = " + lead_office_id
            qapp_annual_criteria = qapp_annual_criteria + "Lead Office = " + Office.objects.get(id=lead_office_id).abbreviation + " and "

            if lead_lab_id is not None and lead_lab_id != '':
                qapp_annual_SQL += " and lab_id = " + lead_lab_id
                qapp_annual_criteria = qapp_annual_criteria + "Lead Center = " + Lab.objects.get(id=lead_lab_id).abbreviation + " and "

                if lead_division_id is not None and lead_division_id != '':
                    qapp_annual_SQL += " and division_id = " + lead_division_id
                    qapp_annual_criteria = qapp_annual_criteria + "Lead Division = " + \
                                            Division.objects.get(id=lead_division_id).abbreviation + " and "

                    if lead_branch_id is not None and lead_branch_id != '':
                        qapp_annual_SQL += " and branch_id = " + lead_branch_id
                        qapp_annual_criteria = qapp_annual_criteria + "Lead Branch = " \
                                                + Branch.objects.get(id=lead_branch_id).abbreviation + " and "

        # Check if user has entered name data for lead/team member/qa managers
        person_last = None
        person_first = None
        if 'lastname' in request.GET:
            person_last = request.GET['lastname']
        if 'firstname' in request.GET:
            person_first = request.GET['firstname']

        if 'roles' in request.GET and (person_last or person_first):
            checked_roles = request.GET.getlist('roles')

            lead_sql = ""
            lead_criteria_list = ""
            if "lead" in checked_roles:
                if person_last:
                    lead_sql = "person_id in (select id from auth_user where upper(last_name) " \
                                       "like upper('" + person_last + "%%'))"
                    lead_criteria_list += "Project Lead Last Name starts with " + str(person_last)

                if person_first:
                    if lead_sql is not "":
                        lead_sql += " and "
                        lead_criteria_list += " and "
                    lead_sql += "person_id in (select id from auth_user where upper(first_name) " \
                                       "like upper('" + person_first + "%%'))"
                    lead_criteria_list += "Project Lead First Name starts with " + str(person_first)

            qam_sql = ""
            qam_criteria_list = ""
            if "qa_manager" in checked_roles:
                if person_last:
                    qam_sql += "qa_manager_id in (select id from auth_user where upper(last_name) " \
                                       "like upper('" + person_last + "%%'))"
                    qam_criteria_list += "Project QA Manager Last Name starts with " + str(person_last)

                if person_first:
                    if qam_sql is not "":
                        qam_sql += " and "
                        qam_criteria_list += " and "
                    qam_sql += "qa_manager_id in (select id from auth_user where upper(first_name) " \
                                       "like upper('" + person_first + "%%'))"
                    qam_criteria_list += "Project QA Manager First Name starts with " + str(person_first)

            reviewer_sql = ""
            reviewer_criteria_list = ""
            if "reviewer" in checked_roles:
                if person_last:
                    reviewer_sql += "reviewer_id in (select id from auth_user where upper(last_name) " \
                                       "like upper('" + person_last + "%%'))"
                    reviewer_criteria_list += "QAPP Reviewer Last Name starts with " \
                                            + str(person_last)

                if person_first:
                    if reviewer_sql is not "":
                        reviewer_sql += " and "
                        reviewer_criteria_list += " and "

                    reviewer_sql += "reviewer_id in (select id from auth_user where upper(first_name) " \
                                       "like upper('" + person_first + "%%'))"
                    reviewer_criteria_list += "QAPP Reviewer First Name starts with " \
                                            + str(person_first)

            people_sql = "("
            people_criteria = "("
            if lead_sql:
                people_sql += lead_sql
                people_criteria += lead_criteria_list

            if qam_sql:
                if people_sql is "(":
                    people_sql += qam_sql
                    people_criteria += qam_criteria_list
                else:
                    people_sql = people_sql + " or " + qam_sql
                    people_criteria = people_criteria + " or " + qam_criteria_list

            if reviewer_sql:
                if people_sql is "(":
                    people_sql += reviewer_sql
                    people_criteria += reviewer_criteria_list
                else:
                    people_sql = people_sql + " or " + reviewer_sql
                    people_criteria = people_criteria + " or " + reviewer_criteria_list

            people_sql += ") "
            people_criteria += ") and "

            qapp_annual_SQL = qapp_annual_SQL + " and " + people_sql
            qapp_annual_criteria = qapp_annual_criteria + people_criteria

            # else no checked roles so ignore person/qa manager/reviewer

        qapp_annual_SQL += " order by p.qa_id"

        if qapp_annual_criteria != "":
            qapp_annual_criteria = qapp_annual_criteria[:-5]
        else:
            qapp_annual_criteria = "no criteria"

        AnnualQAPPReviews = User.objects.raw(qapp_annual_SQL)
        # the_count = len(objs)   # len does not work for raw sql object

        for obj in AnnualQAPPReviews:
            the_count += 1
            obj.curr_qams = get_qamanagers(obj.office_id, obj.lab_id, obj.division_id, obj.branch_id)

        hasResults = True
        query_show = qapp_annual_criteria

    else:
        hasResults = False

    # return HttpResponse(qapp_annual_SQL)

    # return render_to_response('list/list_biennial_sop_review.html', locals(), context_instance=RequestContext(request))

    ############
    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count>0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ProjectsNeedingReview.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            worksheet = workbook.add_worksheet('Annual QAPP Reviews')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "All Projects Needing Annual QAPP Reviews", section_format)

            row += 1
            today = timezone.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "Office", label_format)
            worksheet.write(row, 1, "Center", label_format)
            worksheet.write(row, 2, "Division", label_format)
            worksheet.write(row, 3, "Branch", label_format)
            worksheet.write(row, 4, "Project", label_format)
            worksheet.write(row, 5, "Title", label_format)
            worksheet.write(row, 6, "Approval or Last Review Date", label_format)
            worksheet.write(row, 7, "Project Lead", label_format)
            worksheet.write(row, 8, "Project QA Manager", label_format)
            worksheet.write(row, 9, "Reviewer", label_format)
            worksheet.write(row, 10, "Email Sent", label_format)

            for proj in AnnualQAPPReviews:
                row += 1
                worksheet.write(row, 0, proj.office)
                worksheet.write(row, 1, proj.lab)
                worksheet.write(row, 2, proj.division)
                worksheet.write(row, 3, proj.branch)
                worksheet.write(row, 4, proj.qa_id)
                worksheet.write(row, 5, proj.title)
                if proj.last_qapp_review_date:
                    worksheet.write(row, 6, str(proj.last_qapp_review_date))
                else:
                    worksheet.write(row, 6, str(proj.qapp_approval_date))
                worksheet.write(row, 7, proj.project_lead)
                if proj.qa_manager is not None:
                    worksheet.write(row, 8, proj.qa_manager)
                else:
                    worksheet.write(row, 8, "None")
                if proj.qapp_reviewer is not None:
                    worksheet.write(row, 9, proj.qapp_reviewer)
                else:
                    worksheet.write(row, 9, "None")
                if proj.last_email_sent:
                    worksheet.write(row, 10, str(proj.last_email_sent.date()))

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response


    return render(request, 'list/list_annual_qapp_review.html', locals())



@login_required
@apply_perms
def delete_project_attachment(request, obj_id,**kwargs):
    title = "Delete Project Attachment"
    user = request.user
    project_attachment = get_object_or_404(ProjectAttachment, id=obj_id)
    project = project_attachment.project
    project_id = project.id

    profile = user.userprofile
    obj = get_object_or_404(Project, id=project_id)
    title = "Show Project"

    qlogs = ProjectLog.objects.filter(project=obj)
    project_attachments = ProjectAttachment.objects.filter(project=obj)
    collaborators = obj.collaborators.all()

    if project_attachment.project_log_id is not None:
        url = '/projects/show_expanded/%s/#activity_attachments' % str(project.id)
    else:
        url = '/projects/show_expanded/%s/#attachments' % str(project.id)


    try:
#        if project_attachment.user == user or profile.user_type == "SUPER":
        project_attachment.delete()
        return HttpResponseRedirect(url)
#        else:
#            error = "You are not authorized to delete this attachment."
    except:
        error = "Failed to delete attachment. Please try again."


    return render(request, 'show/show_project.html', locals())


@login_required
@apply_perms
def delete_project_attachment_log(request, obj_id,**kwargs):
    title = "Delete Project Attachment"
    user = request.user
    project_attachment = get_object_or_404(ProjectAttachment, id=obj_id)
    project_log = project_attachment.project_log
    project_log_id = project_log.id
    profile = user.userprofile

    expand_files = True

    try:
#        if project_attachment.user == user or profile.user_type == "SUPER":
        project_attachment.delete()
        url = '/projects/qlog/show_expanded/%s/#attachments' % str(project_log_id)
        return HttpResponseRedirect(url)
#        else:
#            error = "You are not authorized to delete this attachment."
    except:
        error = "Failed to delete attachment. Please try again."


    obj = get_object_or_404(ProjectLog, id=project_log_id)
    project = obj.project

    # Parse weblink to handle multiple links.
    if obj.weblink:
        weblinks_list = obj.weblink.split(' ')
        # Remove any blank entries created by multiple spaces in a row.
        for link in weblinks_list:
            if link == '':
                weblinks_list.remove('')

    pl_qa_log_number_type = obj.project_log_type.abbreviation
    pl_qa_log_number_x = obj.qa_log_number_x
    pl_qa_log_number_y = obj.qa_log_number_y

    x_plus_one = int(pl_qa_log_number_x) + 1
    y_plus_one = int(pl_qa_log_number_y) + 1
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) &
                                                    Q(project_log_type__the_name='QAPP')).count()
    title = "Show QA Activity"
    if obj.project_log_type.the_name == 'QAPP':
        is_not_qapp = False
    else:
        is_not_qapp = True

    if obj.review_type is not None or obj.qa_review_comment is not None:
        has_review = True
    else:
        has_review = False

    clone_x = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(x_plus_one) + '-' + str(0)
    clone_y = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(pl_qa_log_number_x) + '-' + str(y_plus_one)

    clone_x_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)
    clone_y_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)

    qlogs = ProjectLog.objects.filter(project=project)
    the_count = ProjectLog.objects.filter(project=project).count()
    project_attachments = ProjectAttachment.objects.filter(project_log=obj)

    return render(request, 'show/show_project_log.html', locals())




@login_required
@apply_perms
def list_projects(request,**kwargs):
    user = request.user
    title = "Project List"
    projects = []
    labs = get_labs(user)
    lab = get_lab(user)
    if labs > 0:
        for l in labs:
            projs = Project.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation))
            for p in projs:
                projects.append(p)
                the_count = len(projects)
    if not labs:
        projs = Project.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation))
        projects.append(projs)
        the_count = len(projects)

    return render(request, 'list/list_projects.html', locals())



@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@apply_perms
def show_project(request, project_id,**kwargs):
    user = request.user
    profile = user.userprofile
    obj = get_object_or_404(Project, id=project_id)
    title = "Show Project"

    expand_files = False

    orgs = Project_Orgs.objects.filter(project=obj)
    project_update_history = Project_update_history.objects.filter(project=obj)
    qlogs = ProjectLog.objects.filter(project=obj).order_by('project_log_type', 'qa_log_number_x', 'qa_log_number_y')

    related_sops = SOPTab.objects.filter(projects=obj).order_by('sop_number')
    related_notebooks = NotebooksTab.objects.filter(projects=obj).order_by('nb_number')

    collaborators = obj.collaborators.all()

    # Parse weblink to handle multiple links.
    if obj.weblink:
        weblinks_list = obj.weblink.split(' ')
        # Remove any blank entries created by multiple spaces in a row.
        for link in weblinks_list:
            if link == '':
                weblinks_list.remove('')

    have_latest_word_doc = False
    have_latest_pdf = False

    project_attachments = ProjectAttachment.objects.filter(project=obj, where_from='Project')

    for att in project_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    activity_attachments = ProjectAttachment.objects.filter(project=obj).exclude(where_from='Project') \
        .order_by('project_log__project_log_type__abbreviation', 'project_log__qa_log_number_x', 'project_log__qa_log_number_y')

    if obj.restrict_ext_package_files or obj.restrict_qapp_files:

        latest_ep_qlog = get_latest_ep(ProjectLog.objects.filter(Q(project=obj) & Q(project_log_type__the_name='Extramural Package')))

        eligable_users = get_project_users(project=obj)
        if kwargs["allow_edit"]:
            eligable_users.append(user)

        for att in activity_attachments:

            if att.project_log == latest_ep_qlog and obj.restrict_ext_package_files and user not in eligable_users:
                att.restricted = True
                att.restricted_ep = True

            if att.project_log.project_log_type.the_name == 'QAPP' and obj.restrict_qapp_files and user not in eligable_users:
                att.restricted = True
                att.restricted_qapp = True

    for att in activity_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    for att in project_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    # We show the horrible banner if the project is active, has QAPP Status==QAPP Approved, and doesn't identify the latest doc and pdf.
    # There are projects with null status, so check they exist before dereferencing.
    if obj.project_status and obj.qapp_status:
        if obj.project_status.the_name == 'Active' and obj.qapp_status.the_name == 'QAPP Approved' and ( not have_latest_word_doc or not have_latest_pdf ):
            show_horrible_banner = True
            if not have_latest_word_doc and not have_latest_pdf:
                if project_attachments or activity_attachments:
                    missing_att_warning = "This project does not have attachments marked as the latest approved QAPP Word Document or PDF."
                else:
                    missing_att_warning = "This project does not have any attachments. Upload the latest approved QAPP files to the project or the appropriate QA activity and toggle N to Y to indicate they are the latest approved QAPP Word Document and PDF."
            elif not have_latest_word_doc:
                missing_att_warning = "This project does not have an attachment marked as the latest approved QAPP Word Document."
            elif not have_latest_pdf:
                missing_att_warning = "This project does not have an attachment marked as the latest approved QAPP PDF."

    return render(request, 'show/show_project.html', locals())


@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@apply_perms
def show_project_expanded(request, project_id,**kwargs):
    user = request.user
    profile = user.userprofile
    obj = get_object_or_404(Project, id=project_id)
    title = "Show Project"

    expand_files = True

    orgs = Project_Orgs.objects.filter(project=obj)
    project_update_history = Project_update_history.objects.filter(project=obj)
    qlogs = ProjectLog.objects.filter(project=obj).order_by('project_log_type', 'qa_log_number_x', 'qa_log_number_y')

    related_sops = SOPTab.objects.filter(projects=obj).order_by('sop_number')
    related_notebooks = NotebooksTab.objects.filter(projects=obj).order_by('nb_number')

    collaborators = obj.collaborators.all()

    # Parse weblink to handle multiple links.
    if obj.weblink:
        weblinks_list = obj.weblink.split(' ')
        # Remove any blank entries created by multiple spaces in a row.
        for link in weblinks_list:
            if link == '':
                weblinks_list.remove('')

    have_latest_word_doc = False
    have_latest_pdf = False

    project_attachments = ProjectAttachment.objects.filter(project=obj, where_from='Project')

    for att in project_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    activity_attachments = ProjectAttachment.objects.filter(project=obj).exclude(where_from='Project') \
        .order_by('project_log__project_log_type__abbreviation', 'project_log__qa_log_number_x', 'project_log__qa_log_number_y')

    if obj.restrict_ext_package_files or obj.restrict_qapp_files:

        latest_ep_qlog = get_latest_ep(ProjectLog.objects.filter(Q(project=obj) & Q(project_log_type__the_name='Extramural Package')))

        eligable_users = get_project_users(project=obj)
        if kwargs["allow_edit"]:
            eligable_users.append(user)

        for att in activity_attachments:

            if att.project_log == latest_ep_qlog and obj.restrict_ext_package_files and user not in eligable_users:
                att.restricted = True
                att.restricted_ep = True

            if att.project_log.project_log_type.the_name == 'QAPP' and obj.restrict_qapp_files and user not in eligable_users:
                att.restricted = True
                att.restricted_qapp = True

    for att in activity_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    for att in project_attachments:
        att.attachment_type = get_file_type(att.the_name)
        if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
            have_latest_word_doc = True
        if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
            have_latest_pdf = True

    # We show the horrible banner if the project is active, has QAPP Status==QAPP Approved, and doesn't identify the latest doc and pdf.
    # There are projects with null status, so check they exist before dereferencing.
    if obj.project_status and obj.qapp_status:
        if obj.project_status.the_name == 'Active' and obj.qapp_status.the_name == 'QAPP Approved' and ( not have_latest_word_doc or not have_latest_pdf ):
            show_horrible_banner = True
            if not have_latest_word_doc and not have_latest_pdf:
                if project_attachments or activity_attachments:
                    missing_att_warning = "This project does not have attachments marked as the latest approved QAPP Word Document or PDF."
                else:
                    missing_att_warning = "This project does not have any attachments. Upload the latest approved QAPP files to the project or the appropriate QA activity and toggle N to Y to indicate they are the latest approved QAPP Word Document and PDF."
            elif not have_latest_word_doc:
                missing_att_warning = "This project does not have an attachment marked as the latest approved QAPP Word Document."
            elif not have_latest_pdf:
                missing_att_warning = "This project does not have an attachment marked as the latest approved QAPP PDF."

    return render(request, 'show/show_project.html', locals())


@login_required
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@apply_perms
def show_project_tree(request,**kwargs):
    user = request.user
    lab_list = json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "lab": obj.lab,
                            "office_id": obj.office.id, "has_projects": True if Project.objects.filter(lab__id=obj.id) else False}
                           for obj in Lab.objects.select_related('office')])
    division_list = json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "division": obj.division,
                            "lab_id": obj.lab.id, "office_id": obj.office.id, "is_active": obj.is_active,
                            "has_projects": True if Project.objects.filter(division__id=obj.id) else False}
                           for obj in Division.objects.select_related('office', 'lab')])
    branch_list = json.dumps([{"id": obj.id, "abbreviation": obj.abbreviation, "branch": obj.branch,
                            "division_id": obj.division.id, "lab_id": obj.lab.id, "office_id": obj.office.id,
                            "is_active": obj.is_active}
                           for obj in Branch.objects.select_related('office', 'lab', 'division')])
    project_list = json.dumps([{"id": obj.id, "qa_id": obj.qa_id, "title": obj.title,
                                "division_id": obj.division.id if obj.division else None,
                                "branch_id": obj.branch.id if obj.branch else None,
                                "project_lead": obj.person.last_name + ", " + obj.person.first_name if obj.person else None,
                                "project_status": obj.project_status.the_name}
                           for obj in Project.objects.select_related('division', 'branch',
                                                                     'person', 'project_status')])
    # activity_list = json.dumps([{"id": obj.id, "qa_log_number": obj.qa_log_number, "title": obj.title,
    #                             "project_id": obj.project.id,
    #                             "activity_poc": obj.technical_lead.last_name + ", " + obj.technical_lead.first_name if obj.technical_lead else None,
    #                             "type": obj.project_log_type.the_name}
    #                         for obj in ProjectLog.objects.select_related('project', 'technical_lead', 'project_log_type')])

    return render(request, 'show/show_project_tree.html', locals())

@login_required
@apply_perms
def show_project_by_log(request, project_log_id,**kwargs):
    user = request.user
    profile = user.userprofile
    project_log = get_object_or_404(ProjectLog, id=project_log_id)
    obj = Project.objects.get(id=project_log.project_id)
    title = "Show Project"

    qlogs = ProjectLog.objects.filter(project=obj)
    project_attachments = ProjectAttachment.objects.filter(project=obj)
    collaborators = obj.collaborators.all()
    return render(request, 'show/show_project.html', locals())

@login_required
@apply_perms
def search_project(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    title = "Search For Projects"
    project_types = ProjectType.objects.all().order_by('the_name')
    project_statuses = ProjectStatus.objects.filter(is_active="Y").order_by('sort_number')
    selected_status = ProjectStatus.objects.filter(the_name="Active").first()
    programs = Program.objects.all().order_by('the_name')
    project_categories = ProjectCategory.objects.all().order_by('the_name')
    qapp_statuses = QappStatus.objects.all().order_by('the_name')
    qa_categories = QaCategory.objects.all().order_by('the_name')
    nrmrl_qapp_requirements = NRMRLQAPPRequirement.objects.all().order_by('the_name')
    vehicle_types = VehicleType.objects.all().order_by('the_name')

    return render(request, 'main/search_projects.html', locals())

@login_required
@apply_perms
def result_search_project(request,**kwargs):
    user = request.user

    query = Q()
    query_show = ''


    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    apply_org_to = request.GET.get("orgr")
    if apply_org_to == 'projects':

        if office_id is not None and office_id != '':
            office = Office.objects.get(id = office_id)
            query = query & (Q(office__id=office_id))
            query_show = query_show + "Project Office = " + str(office.abbreviation) + ", "

        if lab_id is not None and lab_id != '':
            lab = Lab.objects.get(id = lab_id)
            query = query & (Q(lab__id=lab_id))
            query_show = query_show + "Project Center = " + str(lab.abbreviation) + ", "

        if division_id is not None and division_id != '':
            division = Division.objects.get(id = division_id)
            query = query & (Q(division__id=division_id))
            query_show = query_show + "Project Division = " + str(division.abbreviation) + ", "

        if branch_id is not None and branch_id != '':
            branch = Branch.objects.get(id = branch_id)
            query = query & (Q(branch__id=branch_id))
            query_show = query_show + "Project Branch = " + str(branch.abbreviation) + ", "

    elif apply_org_to == 'contributors':
        if office_id is not None and office_id != '':
            office = Office.objects.get(id = office_id)
            query = query & (Q(collaborators__userprofile__office__id=office_id) | Q(person__userprofile__office__id=office_id))
            query_show = query_show + "Project Lead/Team Member Office = " + str(office.abbreviation) + ", "

        if lab_id is not None and lab_id != '':
            lab = Lab.objects.get(id = lab_id)
            query = query & (Q(collaborators__userprofile__lab__id=lab_id) | Q(person__userprofile__lab__id=lab_id))
            query_show = query_show + "Project Lead/Team Member Center = " + str(lab.abbreviation) + ", "

        if division_id is not None and division_id != '':
            division = Division.objects.get(id = division_id)
            query = query & (Q(collaborators__userprofile__division__id=division_id) | Q(person__userprofile__division__id=division_id))
            query_show = query_show + "Project Lead/Team Member Division = " + str(division.abbreviation) + ", "

        if branch_id is not None and branch_id != '':
            branch = Branch.objects.get(id = branch_id)
            query = query & (Q(collaborators__userprofile__branch__id=branch_id) | Q(person__userprofile__branch__id=branch_id))
            query_show = query_show + "Project Lead/Team Member Branch = " + str(branch.abbreviation) + ", "

    # ORD RAP Programs
    rap_form_fields = get_rap_fields('form')

    vals = []
    for field_array in rap_form_fields:
        field, column = field_array
        if field in request.GET:
            val = request.GET[field]
            if val:
                vals.append(val)
                nums = re.split(r'; |, |;|,',request.GET[field])
                nums = [str.strip() for str in nums]
                showArray = column.split('_')
                rap = showArray.pop(0).upper()
                show = rap + ' ' + ' '.join(showArray).title() #upper the rap and title the rest
                subquery = Q()
                subquery_show = []
                for num in nums:
                    if num == '*':
                        param1 = {}
                        param2 = {}
                        param1[column + '__isnull'] = True
                        param2[column + '__exact'] = ''
                        subquery = subquery | ( ~Q(**param1) & ~Q(**param2) )

                    elif '*' in num:
                        # We run queries like 5.*2 as regex, so we need to remove regexy chars then treat the . and * appropriatley 5.*2 -> r"^5\..*2"
                        num = re.sub('[^a-zA-Z0-9\.\*-]','',num)
                        regex = r'^' + num.replace('.','\.').replace('*','.*')
                        param = {}
                        param[column + '__regex'] = regex
                        subquery = subquery | Q(**param)

                    else:
                        param = {}
                        param[column + '__contains'] = str(num)
                        subquery = subquery | Q(**param)
                    subquery_show.append(show + ' = ' + str(num))

                query = query & subquery
                query_show = query_show + '(' + ' OR '.join(subquery_show) + '), '


    item_01 = ''
    sub_query_01 = Q()
    sub_query_show_01 = ''
    if 'qa' in request.GET:
        qa = request.GET.getlist('qa')
        if qa:
            for item_01 in qa:
                sub_query_01 = sub_query_01 | Q(qa_category__the_name__exact=item_01)
                sub_query_show_01 = sub_query_show_01 + str(item_01) + ", "

            query = sub_query_01 & query
            query_show = query_show + "QA Category(ies) => " + sub_query_show_01

    item_02 = ''
    sub_query_02 = Q()
    sub_query_show_02 = ''
    if 'qr' in request.GET:
        qr = request.GET.getlist('qr')
        if qr:
            for item_02 in qr:
                sub_query_02 = sub_query_02 | Q(nrmrl_qapp_requirement__the_name__exact=item_02)
                sub_query_show_02 = sub_query_show_02 + str(item_02) + ", "

            query = sub_query_02 & query
            query_show = query_show + "Project Type => " + sub_query_show_02

    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'qs' in request.GET:
        qs = request.GET.getlist('qs')
        if qs:
            for item_03 in qs:
                sub_query_03 = sub_query_03 | Q(qapp_status__the_name__exact=item_03)
                sub_query_show_03 = sub_query_show_03 + str(item_03) + ", "

            query = sub_query_03 & query
            query_show = query_show + "QAPP Status(es) => " + sub_query_show_03

    item_04 = ''
    sub_query_04 = Q()
    sub_query_show_04 = ''
    if 'pr' in request.GET:
        pr = request.GET.getlist('pr')
        if pr and not (len(pr)==1 and pr[0] == ""): # do nothing if only the blank selected
            for item_04 in pr:
                if item_04 != "":
                    sub_query_04 = sub_query_04 | Q(programs__the_name__exact=item_04)
                    sub_query_show_04 = sub_query_show_04 + str(item_04) + ", "

            query = sub_query_04 & query
            query_show = query_show + "Program(s) => " + sub_query_show_04

    if 'institution_name' in request.GET:
        institution_name = request.GET['institution_name']
        if institution_name:
            query = query & (Q(institution_name__icontains=institution_name))
            query_show = query_show + "Name of Contractor/Institution => " + str(institution_name) + ", "

    item_05 = ''
    sub_query_05 = Q()
    sub_query_show_05 = ''
    if 'vt' in request.GET:
        vt = request.GET.getlist('vt')
        if vt:
            for item_05 in vt:
                sub_query_05 = sub_query_05 | Q(vehicle_type__the_name__exact=item_05)
                sub_query_show_05 = sub_query_show_05 + str(item_05) + ", "

            query = sub_query_05 & query
            query_show = query_show + "Vehicle Type(s) => " + sub_query_show_05

    if 'vehicle_number' in request.GET:
        vehicle_number = request.GET['vehicle_number']
        if vehicle_number:
            query = query & (Q(vehicle_number__icontains=vehicle_number))
            query_show = query_show + "Vehicle Number => " + str(vehicle_number) + ", "

    if 'kw' in request.GET:
        kw = request.GET['kw']
        if kw:
            query = query & (Q(keyword__icontains=kw))
            query_show = query_show + "Keyword => " + str(kw) + " "

    # Check if user has entered name data for lead/team member/qa managers
    if 'lead_lastname' in request.GET:
        person_last = request.GET['lead_lastname']
    if 'lead_firstname' in request.GET:
        person_first = request.GET['lead_firstname']

    if 'roles' in request.GET and (person_last or person_first):

        checked_roles = request.GET.getlist('roles')
        person_criteria_list = []
        lead_query = None
        team_member_query = None
        qam_query = None
        previousqam_query = None
        people_query = Q()

        if "lead" in checked_roles:
            lead_query = Q()
            lead_criteria_list = []
            if person_last:
                lead_query = lead_query & (Q(person__last_name__istartswith=person_last))
                lead_criteria_list.append("Project Lead Last Name starts with " + str(person_last))

            if person_first:
                lead_query = lead_query & (Q(person__first_name__istartswith=person_first))
                lead_criteria_list.append("Project Lead First Name starts with " + str(person_first))

            lead_criteria = ' and '.join(lead_criteria_list)
            person_criteria_list.append(lead_criteria)
            people_query = people_query | lead_query

        if "team_member" in checked_roles:
            team_member_query = Q()
            team_member_criteria_list = []
            if person_last:
                team_member_query = team_member_query & (Q(collaborators__last_name__istartswith=person_last))
                team_member_criteria_list.append("Team Member Last Name starts with " + str(person_last))

            if person_first:
                team_member_query = team_member_query & (Q(collaborators__first_name__istartswith=person_first))
                team_member_criteria_list.append("Team Member First Name starts with " + str(person_first))

            team_member_criteria = ' and '.join(team_member_criteria_list)
            person_criteria_list.append(team_member_criteria)
            people_query = people_query | team_member_query

        if "qa_manager" in checked_roles:
            qam_query = Q()
            qam_criteria_list = []
            if person_last:
                qam_query = qam_query & (Q(qa_manager__last_name__istartswith=person_last))
                qam_criteria_list.append("QA Manager Last Name starts with " + str(person_last))

            if person_first:
                qam_query = qam_query & (Q(qa_manager__first_name__istartswith=person_first))
                qam_criteria_list.append("QA Manager First Name starts with " + str(person_first))

            qam_criteria = ' and '.join(qam_criteria_list)
            person_criteria_list.append(qam_criteria)
            people_query = people_query | qam_query

        if "previous_qam" in checked_roles:
            previousqam_query = Q()
            previousqam_criteria_list = []
            if person_last:
                previousqam_query = previousqam_query & (Q(previous_qams__last_name__istartswith=person_last))
                previousqam_criteria_list.append("Previous QA Manager Last Name starts with " + str(person_last))

            if person_first:
                previousqam_query = previousqam_query & (Q(previous_qams__first_name__istartswith=person_first))
                previousqam_criteria_list.append("Previous QA Manager First Name starts with " + str(person_first))

            previousqam_criteria = ' and '.join(previousqam_criteria_list)
            person_criteria_list.append(previousqam_criteria)

            people_query = people_query | previousqam_query

        if person_criteria_list:
            query = query & people_query
            query_show += '(' + ' or '.join(person_criteria_list) + '), '
        # else no checked roles so ignore person/team_member/qa managers


    # Date Project Identified From
    if 'c' in request.GET:
        c = request.GET['c']
        if c:
            query = query & (Q(date_project_identified__gte=c))
            query_show = query_show + "Project Identified From Date = " + str(c) + ", "

    # Date Project Identified To
    if 'd' in request.GET:
        d = request.GET['d']
        if d:
            query = query & (Q(date_project_identified__lte=d))
            query_show = query_show + "Project Identified To Date = " + str(d) + ", "

    # Project QA ID
    if 'project_qa_id' in request.GET:
        project_qa_id = request.GET['project_qa_id']
        project_qa_id = project_qa_id.strip() # Trim white space

        if project_qa_id:
            exact = request.GET['qa_id_exact']
            print(exact)
            if exact == 'Y':
                print('exact search')
                query = query & (Q(qa_id=project_qa_id))
                query_show = query_show + "Project QA ID = " + str(project_qa_id) + ", "
            else:
                print('includes search')
                query = query & (Q(qa_id__icontains=project_qa_id))
                query_show = query_show + "Project QA ID contains " + str(project_qa_id) + ", "

    if 'alt_id' in request.GET:
        alt_id = request.GET['alt_id']
        alt_id = alt_id.strip()  # Trim white space
        if alt_id:
            query = query & (Q(alt_id__icontains=alt_id))
            query_show = query_show + "Alternate ID contains " + str(alt_id) + ", "

    if 'previous_id' in request.GET:
        previous_id = request.GET['previous_id']
        previous_id = previous_id.strip()  # Trim white space
        if previous_id:
            query = query & (Q(previous_id__icontains=previous_id))
            query_show = query_show + "Previous ID contains " + str(previous_id) + ", "

    if 'f' in request.GET:
        f = request.GET['f']
        if f:
            query = query & (Q(title__icontains=f))
            query_show = query_show + "Title contains " + str(f) + ", "

    # Project Status
    item_06 = ''
    sub_query_06 = Q()
    sub_query_show_06 = ''
    if 'project_status' in request.GET:
        project_status = request.GET.getlist('project_status')
        if project_status:
            for item_06 in project_status:
                b_status = ProjectStatus.objects.get(id=item_06)
                sub_query_06 = sub_query_06 | Q(project_status_id=item_06)
                sub_query_show_06 = sub_query_show_06 + b_status.the_name + ", "

            query = sub_query_06 & query
            query_show = query_show + "Project Status(es) => " + sub_query_show_06


    if 'k' in request.GET:
        k = request.GET['k']
        if len(k) > 1:
            query = query & (Q(project_type__the_name__icontains=k))
            query_show = query_show + "Intramural or Extramural = " + str(k) + ", "

    if 'comments' in request.GET:
        comments = request.GET['comments']
        if comments:
            query = query & (Q(the_description__icontains=comments))
            query_show = query_show + "Comments contain \"" + str(comments) + "\""

    projects = (
        Project.objects
            .filter(query)
            .select_related("user", "office", "lab", "division", "branch", "person",
                            "project_category", "project_status", "project_type",
                            "qapp_status", "qa_category",
                            "vehicle_type", "rap_program", "rap_project", "rap_task")
            .prefetch_related("collaborators", "programs", "nrmrl_qapp_requirement",
                              "participating_organizations", "projectlog_set")
            .distinct()
    )

    rap_fields = get_rap_fields()

    for obj in projects:
        obj.rap = []
        for rap in rap_fields:
            valString = getattr(obj,rap)
            if valString != '' and valString is not None:
                valString = str(valString)
                if rap == 'hsrp_rap_extensions':
                    program = 'HSRP Extensions'
                else:
                    program = rap.split('_')[0].upper()
                valueList = sort_rap_numbers(re.split(r'; |, |;|,',valString))
                values = ', '.join(valueList)
                if not values.startswith(program):
                    values = program + ' ' + values
                row = {'values':values}
                obj.rap.append(row)


    the_count = len(projects)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    if 'excel' in request.GET:
        excel = request.GET['excel']
        if excel == "Y":

            response = HttpResponse(content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=projects_searched.xls'
            wb = xlwt.Workbook()
            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                        'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                        'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                        'default': xlwt.Style.default_style}

            sheet = wb.add_sheet('Projects')
            sheet.write(0, 0, 'Center')
            sheet.write(0, 1, 'Division')
            sheet.write(0, 2, 'Branch')

            sheet.write(0, 3, 'Project QA ID')
            sheet.write(0, 4, 'Previous ID')
            sheet.write(0, 5, 'Alternate ID')
            sheet.write(0, 6, 'Project Lead Last Name')
            sheet.write(0, 7, 'Project Lead First Name')
            sheet.write(0, 8, 'Project Lead Email')
            sheet.write(0, 9, 'Title')

            sheet.write(0, 10, 'Program')
            sheet.write(0, 11, 'Status')
            sheet.write(0, 12, 'Intramural or Extramural')

            sheet.write(0, 13, 'QAPP Status')
            sheet.write(0, 14, 'Restrict access to QAPP QA activity attachments')
            sheet.write(0, 15, 'Restrict access to Extramural Package QA activity attachments')
            sheet.write(0, 16, 'QA Category')
            sheet.write(0, 17, 'Project Type')
            sheet.write(0, 18, 'Vehicle Type')

            sheet.write(0, 19, 'Team Members')
            sheet.write(0, 20, 'QA Manager Last Name')
            sheet.write(0, 21, 'QA Manager First Name')
            sheet.write(0, 22, 'Previous QA Managers')
            sheet.write(0, 23, 'EPA Non-ORD Organizations')

            sheet.write(0, 24, 'ACE RAP Numbers')
            sheet.write(0, 25, 'CSS RAP Numbers')
            sheet.write(0, 26, 'SSWR RAP Numbers')
            sheet.write(0, 27, 'HHRA RAP Numbers')
            sheet.write(0, 28, 'HSRP RAP Numbers')
            sheet.write(0, 29, 'HSRP RAP Extensions')
            sheet.write(0, 30, 'SHC RAP Numbers')

            sheet.write(0, 31, 'Date Project Identified')
            sheet.write(0, 32, 'QAPP Approval Date')
            sheet.write(0, 33, 'Latest Annual QAPP Review Date')
            sheet.write(0, 34, 'Vehicle Number')

            sheet.write(0, 35, 'Name of Contractor/Institution')
            sheet.write(0, 36, 'QMP Required')
            sheet.write(0, 37, 'QMP Approval Date')

            sheet.write(0, 38, 'Comments')
            sheet.write(0, 39, 'Links')



            i = 1
            for obj in projects:
                if obj.lab is not None:
                    sheet.write(i, 0, obj.lab.abbreviation)
                else:
                    sheet.write(i, 0, '')

                if obj.division is not None:
                    sheet.write(i, 1, obj.division.abbreviation)
                else:
                    sheet.write(i, 1, '')

                if obj.branch is not None:
                    sheet.write(i, 2, obj.branch.abbreviation)
                else:
                    sheet.write(i, 2, '')

                sheet.write(i, 3, obj.qa_id)
                sheet.write(i, 4, obj.previous_id)
                sheet.write(i, 5, obj.alt_id)

                if obj.person is not None:
                    sheet.write(i, 6, obj.person.last_name)
                    sheet.write(i, 7, obj.person.first_name)
                else:
                    sheet.write(i, 6, '')
                    sheet.write(i, 7, '')

                if obj.person is not None:
                    sheet.write(i, 8, obj.person.email)
                else:
                    sheet.write(i, 8, '')

                sheet.write(i, 9, obj.title)

                programs = ''
                if obj.programs is not None:
                    for p in obj.programs.all():
                        programs += p.the_name + '; '
                    sheet.write(i, 10, programs)
                else:
                    sheet.write(i, 10, '')

                if obj.project_status is not None:
                    sheet.write(i, 11, obj.project_status.the_name)
                else:
                    sheet.write(i, 11, '')

                if obj.project_type is not None:
                    sheet.write(i, 12, obj.project_type.the_name)
                else:
                    sheet.write(i, 12, '')

                if obj.qapp_status is not None:
                    sheet.write(i, 13, obj.qapp_status.the_name)
                else:
                    sheet.write(i, 13, '')

                sheet.write(i, 14, obj.restrict_qapp_files)
                sheet.write(i, 15, obj.restrict_ext_package_files)

                if obj.qa_category is not None:
                    sheet.write(i, 16, obj.qa_category.the_name)
                else:
                    sheet.write(i, 16, '')

                # NRMRL QAPP Requirement was renamed to Project Type in the UI.
                the_nrmrl = []
                if obj.nrmrl_qapp_requirement is not None:
                    for c in obj.nrmrl_qapp_requirement.all():
                        the_nrmrl += c.the_name + ' '
                    sheet.write(i, 17, the_nrmrl)
                else:
                    sheet.write(i, 17, '')

                if obj.vehicle_type is not None:
                    sheet.write(i, 18, obj.vehicle_type.the_name)
                else:
                    sheet.write(i, 18, '')

                # Collaborators are now called Team Members.
                the_list = []
                if obj.collaborators is not None:
                    for c in obj.collaborators.all():
                        the_list += ' ' + c.last_name + ', ' + c.first_name
                    sheet.write(i, 19, the_list)
                else:
                    sheet.write(i, 19, '')

                if obj.qa_manager is not None:
                    sheet.write(i, 20, obj.qa_manager.last_name)
                    sheet.write(i, 21, obj.qa_manager.first_name)
                else:
                    sheet.write(i, 20, '')
                    sheet.write(i, 21, '')

                the_list = []
                if obj.previous_qams is not None:
                    for c in obj.previous_qams.all():
                        the_list += ' ' + c.last_name + ', ' + c.first_name
                    sheet.write(i, 22, the_list)
                else:
                    sheet.write(i, 22, '')


                the_orgs = []
                if obj.participating_organizations is not None:
                    for c in obj.participating_organizations.all():
                        the_orgs += ' ' + c.company
                    sheet.write(i, 23, the_orgs)
                else:
                    sheet.write(i, 23, '')

#                raps = [rap['values'] for rap in obj.rap]
#                sheet.write(i, 16, '; '.join(raps))

                sheet.write(i, 24, ', '.join(sort_rap_numbers(xstr(obj.ace_rap_numbers).split(','))))
                sheet.write(i, 25, ', '.join(sort_rap_numbers(xstr(obj.css_rap_numbers).split(','))))
                sheet.write(i, 26, ', '.join(sort_rap_numbers(xstr(obj.sswr_rap_numbers).split(','))))
                sheet.write(i, 27, ', '.join(sort_rap_numbers(xstr(obj.hhra_rap_numbers).split(','))))
                sheet.write(i, 28, ', '.join(sort_rap_numbers(xstr(obj.hsrp_rap_numbers).split(','))))
                sheet.write(i, 29, ', '.join(sort_rap_numbers(xstr(obj.hsrp_rap_extensions).split(','))))
                sheet.write(i, 30, ', '.join(sort_rap_numbers(xstr(obj.shc_rap_numbers).split(','))))

                sheet.write(i, 31, obj.date_project_identified, style=styles["date"])
                sheet.write(i, 32, obj.qapp_approval_date, style=styles["date"])
                sheet.write(i, 33, obj.last_qapp_review_date, style=styles["date"])
                sheet.write(i, 34, obj.vehicle_number)

                sheet.write(i, 35, obj.institution_name)
                sheet.write(i, 36, obj.qmp_required)
                sheet.write(i, 37, obj.qmp_approval_date, style=styles["date"])

                sheet.write(i, 38, obj.the_description)
                sheet.write(i, 39, obj.weblink)



                i += 1

            sheet1 = wb.add_sheet('Query')
            sheet1.write(1, 0, query_show)
            wb.save(response)
            return response

    return render(request, 'main/search_project_result.html', locals())



@login_required
@apply_perms
def search_project_dbissue(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    project_statuses = ProjectStatus.objects.filter(is_active="Y").order_by('sort_number')
    selected_status = ProjectStatus.objects.filter(the_name="Active").first()

    return render(request, 'main/search_projects_dbissue.html', locals())

@login_required
@apply_perms
def result_search_project_dbissue(request,**kwargs):
    user = request.user

    query = Q()
    query_show = ''

    # Ignore projects with QAPP Status of QAPP Not Required (2), ORD does not have QA Lead (3), Implementing Existing Approved QAPP (5)

    query = ~Q(qapp_status__id__exact=2) & ~Q(qapp_status__id__exact=3) & ~Q(qapp_status__id__exact=5)

    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id=office_id)
        query = query & (Q(office__id=office_id))
        query_show = query_show + "Project Office = " + str(office.abbreviation) + ", "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id=lab_id)
        query = query & (Q(lab__id=lab_id))
        query_show = query_show + "Project Center = " + str(lab.abbreviation) + ", "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id=division_id)
        query = query & (Q(division__id=division_id))
        query_show = query_show + "Project Division = " + str(division.abbreviation) + ", "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id=branch_id)
        query = query & (Q(branch__id=branch_id))
        query_show = query_show + "Project Branch = " + str(branch.abbreviation) + ", "

    # Project Status
    item_06 = ''
    sub_query_06 = Q()
    sub_query_show_06 = ''
    if 'project_status' in request.GET:
        project_status = request.GET.getlist('project_status')

        if project_status:
            for item_06 in project_status:
                b_status = ProjectStatus.objects.get(id=item_06)
                sub_query_06 = sub_query_06 | Q(project_status_id=item_06)
                sub_query_show_06 = sub_query_show_06 + b_status.the_name + ", "

            query = sub_query_06 & query
            query_show = query_show + "Project Status(es) => " + sub_query_show_06

    projects = (
        Project.objects
            .filter(query)
            .select_related("user", "office", "lab", "division", "branch", "person",
                            "project_category", "project_status", "project_type",
                            "qapp_status", "qa_category",
                            "vehicle_type", "rap_program", "rap_project", "rap_task")
            .prefetch_related("collaborators", "programs", "nrmrl_qapp_requirement",
                              "participating_organizations", "projectlog_set")
            .distinct()
    )

    the_count = len(projects)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]


    # Iterate through the projects to check for data quality issues.
    qapp_query = Q(project_log_type__the_name="QAPP") & Q(date_approved__isnull=False) & (
            Q(review_type__the_name="Approved") | Q(review_type__the_name="Approved with minor revisions"))

    wanted_items = set()

    for proj in projects:

        has_issue = False

        # Check if project lead has separated.
        if proj.person is not None:
            if proj.person.userprofile.date_epa_separation is not None:
                has_issue = True


        if has_issue == False:
            # Check if project is missing latest approved QAPP files.
            # Check project attachments first.
            project_attachments = ProjectAttachment.objects.filter(project=proj, where_from='Project')
            have_latest_word_doc = False
            have_latest_pdf = False

            for att in project_attachments:
                att.attachment_type = get_file_type(att.the_name)
                if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
                    have_latest_word_doc = True
                if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
                    have_latest_pdf = True

            if have_latest_word_doc == False or have_latest_pdf == False:
                # Check activity attachments.
                activity_attachments = ProjectAttachment.objects.filter(project=proj).exclude(where_from='Project') \
                    .order_by('project_log__project_log_type__abbreviation', 'project_log__qa_log_number_x',
                              'project_log__qa_log_number_y')
                for att in activity_attachments:
                    att.attachment_type = get_file_type(att.the_name)
                    if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
                        have_latest_word_doc = True
                    if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
                        have_latest_pdf = True
            if have_latest_word_doc == False or have_latest_pdf == False:
                has_issue = True

            if has_issue == False:
                # Check if project is missing approved QAPP QA activity.
                proj_qapps = ProjectLog.objects.filter(qapp_query & Q(project=proj))
                if proj_qapps.count() == 0:
                    has_issue = True

        if has_issue == True:
            wanted_items.add(proj.pk)

    projects = projects.filter(pk__in = wanted_items)
    the_count = len(projects)

    rap_fields = get_rap_fields()




    for proj in projects:
        # add calculated data

        proj.issues = ""

        # RAP projects/Task
        proj.rap = []
        for rap in rap_fields:
            valString = getattr(proj, rap)
            if valString != '' and valString is not None:
                valString = str(valString)
                if rap == 'hsrp_rap_extensions':
                    program = 'HSRP Extensions'
                else:
                    program = rap.split('_')[0].upper()
                valueList = sort_rap_numbers(re.split(r'; |, |;|,', valString))
                values = ', '.join(valueList)
                if not values.startswith(program):
                    values = program + ' ' + values
                row = {'values': values}
                proj.rap.append(row)

        # Check if project lead has separated.
        if proj.person is not None:
            if proj.person.userprofile.date_epa_separation is not None:
                today = timezone.now().date()
                if proj.person.userprofile.date_epa_separation <= today:
                    proj.issues = proj.issues + "Project Lead has separated. "

        # Check if project is missing latest approved QAPP files.
        proj.have_latest_word_doc = 'N'
        proj.have_latest_pdf = 'N'

        # Check project attachments first.
        project_attachments = ProjectAttachment.objects.filter(project=proj, where_from='Project')

        for att in project_attachments:
            att.attachment_type = get_file_type(att.the_name)
            if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
                proj.have_latest_word_doc = 'Y'
            if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
                proj.have_latest_pdf = 'Y'

        if proj.have_latest_word_doc == 'N' or proj.have_latest_pdf == 'N':
            # Check activity attachments.
            activity_attachments = ProjectAttachment.objects.filter(project=proj).exclude(where_from='Project') \
                .order_by('project_log__project_log_type__abbreviation', 'project_log__qa_log_number_x',
                          'project_log__qa_log_number_y')
            for att in activity_attachments:
                att.attachment_type = get_file_type(att.the_name)
                if att.attachment_type == 'doc' and att.is_latest_qapp_doc == 'Y':
                    proj.have_latest_word_doc = 'Y'
                if att.attachment_type == 'pdf' and att.is_latest_qapp_pdf == 'Y':
                    proj.have_latest_pdf = 'Y'

        if proj.have_latest_pdf == "N":
            if proj.have_latest_word_doc == "N":
                proj.issues = proj.issues + "Project does not have a Word or PDF file identified as the latest approved QAPP. "
            else:
                proj.issues = proj.issues + "Project does not have a PDF file identified as the latest approved QAPP. "
        else:
            if proj.have_latest_word_doc == "N":
                proj.issues = proj.issues + "Project does not have a Word file identified as the latest approved QAPP. "

        # Check if project is missing approved QAPP QA activity.
        proj_qapps = ProjectLog.objects.filter(qapp_query & Q(project=proj))
        if proj_qapps.count() == 0:
            proj.issues = proj.issues + "Project does not have an approved QAPP activity. If it has a QAPP QA activity, check if it has a Date Approved value and a Review Recommendation of  Approved/Approved with minor revisions."

    ############
    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count>0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ProjectsDBIssues.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            worksheet = workbook.add_worksheet('Projects with Issues')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "Projects With Database Completeness Issues", section_format)

            row += 1
            today = timezone.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "Office", label_format)
            worksheet.write(row, 1, "Center", label_format)
            worksheet.write(row, 2, "Division", label_format)
            worksheet.write(row, 3, "Branch", label_format)
            worksheet.write(row, 4, "Project QA ID", label_format)
            worksheet.write(row, 5, "Title", label_format)
            worksheet.write(row, 6, "RAP Projects/Task", label_format)
            worksheet.write(row, 7, "Database Completeness Issues", label_format)
            worksheet.write(row, 8, "Project Lead", label_format)
            worksheet.write(row, 9, "Project Lead Separation Date", label_format)
            worksheet.write(row, 10, "QA Manager", label_format)
            worksheet.write(row, 11, "Project Status", label_format)
            worksheet.write(row, 12, "QAPP Status", label_format)
            worksheet.write(row, 13, "Has Approved QAPP Word Doc", label_format)
            worksheet.write(row, 14, "Has Approved QAPP PDF", label_format)

            # Placeholders for QAMs to record analysis of projects.
            worksheet.write(row, 15, "Recommended change to QA Track Project Entry")
            worksheet.write(row, 16, "Justification for No Change Recommendations")
            worksheet.write(row, 17, "QA Manager Input Needed to Resolve")


            for proj in projects:
                row += 1
                worksheet.write(row, 0, proj.office.abbreviation)
                if proj.lab:
                    worksheet.write(row, 1, proj.lab.abbreviation)
                else:
                    worksheet.write(row, 1, "")
                if proj.division:
                    worksheet.write(row, 2, proj.division.abbreviation)
                else:
                    worksheet.write(row, 2, "")
                if proj.branch:
                    worksheet.write(row, 3, proj.branch.abbreviation)
                else:
                    worksheet.write(row, 3, "")
                worksheet.write(row, 4, proj.qa_id)
                worksheet.write(row, 5, proj.title)
                rapnums = ""
                for raprow in proj.rap:
                    rapnums = rapnums + " " + raprow['values']
                    worksheet.write(row, 6, rapnums)
                worksheet.write(row, 7, proj.issues)

                if proj.person is not None:
                    worksheet.write(row, 8, proj.person.first_name + " " + proj.person.last_name)
                    if proj.person.userprofile.date_epa_separation:
                        worksheet.write(row, 9, str(proj.person.userprofile.date_epa_separation))
                    else:
                        worksheet.write(row, 9, "")
                else:
                    worksheet.write(row, 8, "")
                    worksheet.write(row, 9, "")

                if proj.qa_manager is not None:
                    worksheet.write(row, 10, proj.qa_manager.first_name + " " + proj.qa_manager.last_name)
                else:
                    worksheet.write(row, 10, "")

                if proj.project_status is not None:
                    worksheet.write(row, 11, proj.project_status.the_name)
                else:
                    worksheet.write(row, 10, "")

                if proj.qapp_status is not None:
                    worksheet.write(row, 12, proj.qapp_status.the_name)
                else:
                    worksheet.write(row, 10, "")

                worksheet.write(row, 13, proj.have_latest_word_doc)
                worksheet.write(row, 14, proj.have_latest_pdf)

            # wrap up - Add a sheet with the query
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, query_show)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response


    return render(request, 'main/search_project_dbissue_result.html', locals())


@login_required
@apply_perms
def search_project_seplead(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    project_statuses = ProjectStatus.objects.filter(is_active="Y").order_by('sort_number')
    selected_status = ProjectStatus.objects.filter(the_name="Active").first()

    return render(request, 'main/search_projects_seplead.html', locals())

@login_required
@apply_perms
def result_search_project_seplead(request,**kwargs):
    user = request.user

    query = Q()
    query_show = ''

    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id=office_id)
        query = query & (Q(office__id=office_id))
        query_show = query_show + "Project Office = " + str(office.abbreviation) + ", "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id=lab_id)
        query = query & (Q(lab__id=lab_id))
        query_show = query_show + "Project Center = " + str(lab.abbreviation) + ", "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id=division_id)
        query = query & (Q(division__id=division_id))
        query_show = query_show + "Project Division = " + str(division.abbreviation) + ", "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id=branch_id)
        query = query & (Q(branch__id=branch_id))
        query_show = query_show + "Project Branch = " + str(branch.abbreviation) + ", "

    # Project Status
    item_06 = ''
    sub_query_06 = Q()
    sub_query_show_06 = ''
    if 'project_status' in request.GET:
        project_status = request.GET.getlist('project_status')

        if project_status:
            for item_06 in project_status:
                b_status = ProjectStatus.objects.get(id=item_06)
                sub_query_06 = sub_query_06 | Q(project_status_id=item_06)
                sub_query_show_06 = sub_query_show_06 + b_status.the_name + ", "

            query = sub_query_06 & query
            query_show = query_show + "Project Status(es) => " + sub_query_show_06

    projects = (
        Project.objects
            .filter(query)
            .select_related("user", "office", "lab", "division", "branch", "person",
                            "project_category", "project_status", "project_type",
                            "qapp_status", "qa_category",
                            "vehicle_type", "rap_program", "rap_project", "rap_task")
            .prefetch_related("collaborators", "programs", "nrmrl_qapp_requirement",
                              "participating_organizations", "projectlog_set")
            .distinct()
    )

    the_count = len(projects)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    wanted_items = set()

    for proj in projects:

        has_issue = False

        # Check if project lead has separated.
        if proj.person is not None:
            if proj.person.userprofile.date_epa_separation is not None:
                today = timezone.now().date()
                if proj.person.userprofile.date_epa_separation <= today:
                    has_issue = True

        if has_issue == True:
            wanted_items.add(proj.pk)

    projects = projects.filter(pk__in = wanted_items)
    the_count = len(projects)

    rap_fields = get_rap_fields()

    for proj in projects:
        # add calculated data

        proj.issues = ""

        # RAP projects/Task
        proj.rap = []
        for rap in rap_fields:
            valString = getattr(proj, rap)
            if valString != '' and valString is not None:
                valString = str(valString)
                if rap == 'hsrp_rap_extensions':
                    program = 'HSRP Extensions'
                else:
                    program = rap.split('_')[0].upper()
                valueList = sort_rap_numbers(re.split(r'; |, |;|,', valString))
                values = ', '.join(valueList)
                if not values.startswith(program):
                    values = program + ' ' + values
                row = {'values': values}
                proj.rap.append(row)


    ############
    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count>0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=ProjectsSeparatedLead.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            worksheet = workbook.add_worksheet('Projects with Separated Lead')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "Projects with Separated Project Lead Only", section_format)

            row += 1
            today = timezone.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "Office", label_format)
            worksheet.write(row, 1, "Center", label_format)
            worksheet.write(row, 2, "Division", label_format)
            worksheet.write(row, 3, "Branch", label_format)
            worksheet.write(row, 4, "Project QA ID", label_format)
            worksheet.write(row, 5, "Title", label_format)
            worksheet.write(row, 6, "RAP Projects/Task", label_format)
            worksheet.write(row, 7, "Project Lead", label_format)
            worksheet.write(row, 8, "Project Lead Separation Date", label_format)
            worksheet.write(row, 9, "QA Manager", label_format)
            worksheet.write(row, 10, "Project Status", label_format)


            for proj in projects:
                row += 1
                worksheet.write(row, 0, proj.office.abbreviation)
                if proj.lab:
                    worksheet.write(row, 1, proj.lab.abbreviation)
                else:
                    worksheet.write(row, 1, "")
                if proj.division:
                    worksheet.write(row, 2, proj.division.abbreviation)
                else:
                    worksheet.write(row, 2, "")
                if proj.branch:
                    worksheet.write(row, 3, proj.branch.abbreviation)
                else:
                    worksheet.write(row, 3, "")
                worksheet.write(row, 4, proj.qa_id)
                worksheet.write(row, 5, proj.title)
                rapnums = ""
                for raprow in proj.rap:
                    rapnums = rapnums + " " + raprow['values']
                    worksheet.write(row, 6, rapnums)
                worksheet.write(row, 7, proj.person.first_name + " " + proj.person.last_name)
                if proj.person.userprofile.date_epa_separation:
                    worksheet.write(row, 8, str(proj.person.userprofile.date_epa_separation))
                else:
                    worksheet.write(row, 8, "")

                if proj.qa_manager is not None:
                    worksheet.write(row, 9, proj.qa_manager.first_name + " " + proj.qa_manager.last_name)
                else:
                    worksheet.write(row, 9, "")

                worksheet.write(row, 10, proj.project_status.the_name)

            # wrap up - Add a sheet with the query
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, query_show)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response

    return render(request, 'main/search_project_seplead_result.html', locals())


@login_required
@apply_perms
def search_projects_for_last_60(request,**kwargs):
    user = request.user
    query = Q()
    query_show = 'Date Project Identified For Last 60 Days'
    project_types = ProjectType.objects.all().order_by('the_name')
    project_statuses = ProjectStatus.objects.all().order_by('the_name')

    title = "New Projects Last 60 Days - With Results Shown"
    d = datetime.today() - timedelta(days=60)

    projects = []
    labs = get_labs(user)
    lab = get_lab(user)
    if labs is not None:
        for l in labs:
            projs = Project.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation) & Q(date_project_identified__gte=d))
            for p in projs:
                projects.append(p)
                the_count = len(projects)
    if not labs:
        projects = Project.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_project_identified__gte=d))
        the_count = Project.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_project_identified__gte=d)).count()

    return render(request, 'main/search_projects.html', locals())




####################################################################### End Project




###################################################################################################################################### Start QA Activity (Project Log)
###################################################################################################################################### Start QA Activity (Project Log)
###################################################################################################################################### Start QA Activity (Project Log)
###################################################################################################################################### Start QA Activity (Project Log)


@login_required
@apply_perms
def create_project_log(request, obj_id, tlp_id, send_error=None,**kwargs):
    user = request.user
    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Activities"
#    else:
#        error_message = "You are not authorized to create QA Activities."
#        back_link = "/projects/qlog/search/"
#        return render(request, 'error.html', locals())

    if send_error == '1':
        error_message = "This QA Log Number has already been used, please check the list to the left of this form to see what numbers have been used."
    else:
        error_message = ''

    project = Project.objects.get(id=obj_id)
    title = "Create a New QA Activity For Project: " + project.title
    technical_lead = Person.objects.get(id=tlp_id)
    project_logs = ProjectLog.objects.filter(project=project)
    project_logs_count = ProjectLog.objects.filter(project=project).count()

    if project_logs_count == 0:
        init_x = 1
        init_y = 0
    else:
        init_x = ""
        init_y = ""

    if request.method == "POST":
        form = ProjectLogFormAsync(data=request.POST, files=request.FILES, initial={'qa_log_number_x':init_x, 'qa_log_number_y':init_y})
        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            project_log = form.save(commit=False)
            if project_log.title == '':
                project_log.title = project.title

            if project_log.date_received == '':
                project_log.date_received = None
            if project_log.date_reviewed == '':
                project_log.date_reviewed = None
            if project_log.date_approved == '':
                project_log.date_approved = None
            if project_log.qa_review_date == '':
                project_log.qa_review_date = None


            project_log.qa_log_number = str(project.qa_id) + "-" + project_log.project_log_type.abbreviation + "-" + str(project_log.qa_log_number_x) + "-" + str(project_log.qa_log_number_y)
            log_count = ProjectLog.objects.filter(qa_log_number=project_log.qa_log_number).count()

            if log_count > 1:
                url = '/projects/qlog/create/%s/%s/%s/' % (str(project.id), str(technical_lead.id), tr('1'))
                return HttpResponseRedirect(url)

            project_log.user = user
            project_log.created_by = user.username
            project_log.last_modified_by = user.username
            project_log.project = project
            project_log.technical_lead = technical_lead
            project_log.division = project.division
            try:
                project_log.branch = project.branch
            except:
                pass
            project_log.qa_id = project.qa_id
            project_log.save()

            if project_log.project_log_type.the_name == 'QAPP':

                if project_log.date_received is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
                else:
                    pass

                if project_log.date_reviewed is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
                else:
                    pass

                if project_log.date_approved is not None:
                    project.qapp_approval_date = project_log.date_approved
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
                else:
                    pass
                project.save()

            else:
                pass


            url = '/projects/qlog/show/%s/' % str(project_log.id)
            return HttpResponseRedirect(url)
    else:
        form = ProjectLogFormAsync(initial={'qa_log_number_x':init_x, 'qa_log_number_y':init_y})
    return render(request, 'create.html', locals())

@login_required
@apply_perms
def clone_project_log(request, project_log_id,**kwargs):
    user = request.user
    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Activities"
#    else:
#        error_message = "You are not authorized to create QA Activities."
#        back_link = "/projects/qlog/search/"
#        return render(request, 'error.html', locals())

    obj = ProjectLog.objects.get(id=project_log_id)
    pl = ProjectLog.objects.get(id=project_log_id)
    pl_qa_log_number_x = pl.qa_log_number.split('-')[4]
    pl_qa_log_number_y = pl.qa_log_number.split('-')[5]
    project = pl.project
    project_logs = ProjectLog.objects.filter(project=project)
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) & Q(project_log_type__the_name="QAPP")).count()

    new_project_log = ProjectLog.objects.create(project=pl.project, project_log_type=pl.project_log_type)

    new_project_log.office = pl.office
    new_project_log.lab = pl.lab
    new_project_log.division = pl.division
    new_project_log.branch = pl.branch
    new_project_log.user=pl.user
    new_project_log.technical_lead=pl.technical_lead
    new_project_log.reviewer=pl.reviewer
    new_project_log.the_name=pl.the_name
    new_project_log.title=pl.title
    new_project_log.the_description=pl.the_description
    new_project_log.weblink=pl.weblink
    new_project_log.qa_id=pl.qa_id
    new_project_log.recommendation=pl.recommendation
    new_project_log.attachment=pl.attachment
    new_project_log.attachment_02=pl.attachment_02

    new_project_log.lco_tracking_number=pl.lco_tracking_number
    new_project_log.qa_review_required=pl.qa_review_required
    new_project_log.qapp = pl.qapp
    new_project_log.product_category = pl.product_category
    new_project_log.organization=pl.organization
    new_project_log.software_status=pl.software_status
    new_project_log.public_or_private=pl.public_or_private
    new_project_log.last_modified_by = user.username


    new_project_log.qa_log_number_x=int(pl_qa_log_number_x)
    new_project_log.qa_log_number_y=int(pl_qa_log_number_y) + 1

    new_project_log.qa_log_number=str(pl.qa_id) + "-" + pl.project_log_type.abbreviation + "-" + str(new_project_log.qa_log_number_x) + "-" + str(int(new_project_log.qa_log_number_y))
    new_project_log.save()

    log_count = ProjectLog.objects.filter(qa_log_number=new_project_log.qa_log_number).count()
    while log_count > 1:
        new_project_log.qa_log_number_y = new_project_log.qa_log_number_y + 1
        new_project_log.qa_log_number = str(project.qa_id) + "-" + new_project_log.project_log_type.abbreviation + "-" + str(new_project_log.qa_log_number_x) + "-" + str(new_project_log.qa_log_number_y)
        log_count = ProjectLog.objects.filter(qa_log_number=new_project_log.qa_log_number).count()
        if log_count == 1:
            new_project_log.qa_log_number_y = new_project_log.qa_log_number_y + 1

    new_project_log.qa_log_number = str(project.qa_id) + "-" + new_project_log.project_log_type.abbreviation + "-" + str(new_project_log.qa_log_number_x) + "-" + str(new_project_log.qa_log_number_y)
    new_project_log.save()
    obj = new_project_log

    # Create an update history entry for creation.
    comment = 'QA activity created by cloning' # pl.qa_log_number
    projectlog_update_history = ProjectLog_update_history.objects.create(project_log=new_project_log,
                                                                         user=user,
                                                                         date_approved=new_project_log.date_approved,
                                                                         review_type=new_project_log.review_type,
                                                                         technical_lead=new_project_log.technical_lead,
                                                                         reviewer=new_project_log.reviewer,
                                                                         comments=comment)

    if new_project_log.project_log_type.the_name == 'QAPP':

        if new_project_log.date_received is not None:
            project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
        else:
            pass

        if new_project_log.date_reviewed is not None:
            project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
        else:
            pass

        if new_project_log.date_approved is not None:
            project.qapp_approval_date = new_project_log.date_approved
            project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
        else:
            pass

        project.save()

    else:
        pass

    url = '/projects/qlog/edit/%s/' % str(new_project_log.id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def clone_project_log_y(request, project_log_id,**kwargs):
    user = request.user
    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Activities"
#    else:
#        error_message = "You are not authorized to create QA Activities."
#        back_link = "/projects/qlog/search/"
#        return render(request, 'error.html', locals())

    obj = ProjectLog.objects.get(id=project_log_id)
    pl = ProjectLog.objects.get(id=project_log_id)
    project = pl.project
    pl_qa_log_number_x = pl.qa_log_number.split('-')[4]
    pl_qa_log_number_y = pl.qa_log_number.split('-')[5]
    project_logs = ProjectLog.objects.filter(project=project)
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) & Q(project_log_type__the_name="QAPP")).count()

    new_project_log = ProjectLog.objects.create(project=pl.project, division=pl.division, branch=pl.branch, project_log_type=pl.project_log_type)

    new_project_log.user=pl.user
    new_project_log.technical_lead=pl.technical_lead
    new_project_log.reviewer=pl.reviewer
    new_project_log.the_name=pl.the_name
    new_project_log.title=pl.title
    new_project_log.the_description=pl.the_description
    new_project_log.weblink=pl.weblink
    new_project_log.qa_id=pl.qa_id
    new_project_log.recommendation=pl.recommendation
    new_project_log.attachment=pl.attachment
    new_project_log.attachment_02=pl.attachment_02

    new_project_log.lco_tracking_number=pl.lco_tracking_number
    new_project_log.qa_review_required=pl.qa_review_required
    new_project_log.organization=pl.organization
    new_project_log.software_status=pl.software_status
    new_project_log.public_or_private=pl.public_or_private

    if new_project_log.project_log_type.abbreviation == 'QP':
        new_project_log.qa_log_number_x = int(1)
        new_project_log.qa_log_number_y = project_qapps_count
    else:
        new_project_log.qa_log_number_x=int(pl_qa_log_number_x) + 1
        new_project_log.qa_log_number_y=0

    new_project_log.qa_log_number=str(pl.qa_id) + "-" + pl.project_log_type.abbreviation + "-" + str(int(new_project_log.qa_log_number_x)) + "-" + str(0)
    new_project_log.save()

    log_count = ProjectLog.objects.filter(qa_log_number=new_project_log.qa_log_number).count()
    while log_count > 1:
        new_project_log.qa_log_number_y = new_project_log.qa_log_number_y + 1
        new_project_log.qa_log_number = str(project.qa_id) + "-" + new_project_log.project_log_type.abbreviation + "-" + str(new_project_log.qa_log_number_x) + "-" + str(new_project_log.qa_log_number_y)
        log_count = ProjectLog.objects.filter(qa_log_number=new_project_log.qa_log_number).count()
        if log_count == 1:
            new_project_log.qa_log_number_y = new_project_log.qa_log_number_y + 1

    new_project_log.qa_log_number = str(project.qa_id) + "-" + new_project_log.project_log_type.abbreviation + "-" + str(new_project_log.qa_log_number_x) + "-" + str(new_project_log.qa_log_number_y)
    new_project_log.save()
    obj = new_project_log

    if new_project_log.project_log_type.the_name == 'QAPP':

        if new_project_log.date_received is not None:
            project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
        else:
            pass

        if new_project_log.date_reviewed is not None:
            project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
        else:
            pass

        if new_project_log.date_approved is not None:
            project.qapp_approval_date = new_project_log.date_approved
            project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
        else:
            pass

        project.save()

    else:
        pass

    url = '/projects/qlog/edit/%s/' % str(new_project_log.id)
    return HttpResponseRedirect(url)

# This is called when you click on Create a QA Activity from the QA ACtivity tab.
@login_required
@apply_perms
def create_project_log_no_project(request,**kwargs):
    user = request.user
    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Activities"
#    else:
#        error_message = "You are not authorized to create QA Activities."
#        back_link = "/projects/qlog/search/"
#        return render(request, 'error.html', locals())

    title = "Create a New QA Activity For Project: "

    ## get the list of projects to associate the QA activity with
    projects = []

    office_list = oq.get_office_list(user, as_json=True)
    labs = oq.get_lab_list(user, None)

    projects = Project.objects.filter(Q(lab__id__in=[lab.id for lab in labs]) &
                                      Q(project_status__the_name="Active")).all()
    the_count = len(projects)

    return render(request, 'list/select_project_for_log.html', locals())

#
# Called when creating a QA activity and don't know activity type
# Using action "Add QA Activity to this project"
#
@login_required
@apply_perms
def create_project_log_no_tlp(request, obj_id, send_error=None,**kwargs):
    user = request.user
    profile = user.userprofile

    # get the organization data
    office_list = oq.get_office_list(user, as_json=True)
    lab_list = oq.get_lab_list(user, None, as_json=True)
    division_list = oq.get_division_list(user, None, None, as_json=True)
    branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

    poc_list_objs = (
        UserProfile.objects
            .select_related("user","office","lab","division","branch")
            .all()
    )
    poc_list = json.dumps([{"id": obj.id, "user_id": obj.user.id, "office_id": obj.office.id if obj.office else 0,
                            "lab_id": obj.lab.id if obj.lab else 0,
                            "division_id": obj.division.id if obj.division else 0,
                            "branch_id": obj.branch.id if obj.branch else 0}
                           for obj in poc_list_objs])

    # formatting for the organization selector
    office_required = True
    lab_required = True
    division_required = True
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    user_list = User.objects.order_by("last_name").all()
#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Activities"
#    else:
#        error_message = "You are not authorized to create QA Activities."
#        back_link = "/projects/qlog/search/"
#        return render(request, 'error.html', locals())

    project = Project.objects.get(id=obj_id)
    title = "Create a New QA Activity For Project: QA ID:" + project.qa_id + ", Name: " +project.title

    if send_error == '1':
        error_message = "This QA Activity Number has already been used, please check the list at the bottom of this form to see what numbers have been used."
    else:
        error_message = ''

    project_logs = ProjectLog.objects.filter(project=project).select_related("project_log_type")
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) & Q(project_log_type__the_name='QAPP')).count()

    project_logs_count = ProjectLog.objects.filter(project=project).count()
    if project_logs_count == 0:
        init_x = 1
        init_y = 0
    else:
        init_x = ""
        init_y = ""

    if request.method == "POST":
        print('POST')

        form = ProjectLogNoProjectFormAsync(data=request.POST, files=request.FILES, initial={'qa_log_number_x':init_x, 'qa_log_number_y':init_y, 'project': project})

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        selected_office = Office.objects.get(id = office_id) if oq._valid_org_id(office_id) else None
        selected_lab = Lab.objects.get(id = lab_id) if oq._valid_org_id(lab_id) else None
        selected_division = Division.objects.get(id = division_id) if oq._valid_org_id(division_id) else None
        selected_branch = Branch.objects.get(id = branch_id) if oq._valid_org_id(branch_id) else None

        # These are used for deciding if a project update history entry should be created.
        before_qapp_status = project.qapp_status
        before_qapp_approval_date = project.qapp_approval_date
        before_last_qapp_review_date = project.last_qapp_review_date

        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            project_log = form.save(commit=False)
            if project_log.title == '':
                project_log.title = project.title

            if project_log.date_received == '':
                project_log.date_received = None
            if project_log.date_reviewed == '':
                project_log.date_reviewed = None
            if project_log.date_approved == '':
                project_log.date_approved = None
            if project_log.date_review_requested == '':
                project_log.date_review_requested = None

            if project_log.project_log_type.abbreviation == 'QP' and project_log.qa_log_number_x != 1:
                project_log.qa_log_number_x = 1
                project_log.qa_log_number_y = project_qapps_count

            project_log.qa_log_number = str(project.qa_id) + "-" + project_log.project_log_type.abbreviation + "-" + str(project_log.qa_log_number_x) + "-" + str(project_log.qa_log_number_y)
            log_count = ProjectLog.objects.filter(qa_log_number=project_log.qa_log_number).count()

            if log_count > 0:
                url = '/projects/qlog/add/%s/%s/' % (str(project.id), str('1'))
                return HttpResponseRedirect(url)

            project_log.user = user
            project_log.created_by = user.username
            project_log.last_modified_by = user.username
            project_log.project = project
            project_log.qa_id = project.qa_id

            project_log.save()

            update_comments = ''

            # Check if project fields should be updated as a result of a QAPP QA activity update.
            if project_log.project_log_type.the_name == 'QAPP':

                if project_log.date_received is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
                else:
                    pass

                if project_log.date_reviewed is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
                else:
                    pass

                if project_log.date_approved is not None:
                    project.qapp_approval_date = project_log.date_approved
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
                    if project.last_qapp_review_date is not None:
                        if project_log.date_approved > project.last_qapp_review_date:
                            project.last_qapp_review_date = project_log.date_approved
                    else:
                        project.last_qapp_review_date = project_log.date_approved
                else:
                    pass

                project.save()

                # Add entry to project update history if project's fields changed (Only for QAPP QA activities).
                log_hist = False

                if before_qapp_status != project.qapp_status:
                    log_hist = True
                elif before_qapp_approval_date != project.qapp_approval_date:
                    log_hist = True
                elif before_last_qapp_review_date != project.last_qapp_review_date:
                    log_hist = True

                if log_hist:
                    update_comments = 'QAPP QA activity created'

                    # add to project update history
                    project_update_history = Project_update_history.objects.create(project=project,
                                                                                   user=user,
                                                                                   date_qappreviewed=project.last_qapp_review_date,
                                                                                   projectlead=project.person,
                                                                                   qa_manager=project.qa_manager,
                                                                                   project_status=project.project_status,
                                                                                   qapp_status=project.qapp_status,
                                                                                   comments=update_comments)

            else:
                pass

            # add entry to QA activity update history
            if update_comments == '':
                update_comments = 'QA activity created'
            projectlog_update_history = ProjectLog_update_history.objects.create(project_log=project_log,
                                                                                 user=user,
                                                                                 date_approved=project_log.date_approved,
                                                                                 review_type=project_log.review_type,
                                                                                 technical_lead=project_log.technical_lead,
                                                                                 reviewer=project_log.reviewer,
                                                                                 comments=update_comments)

            url = '/projects/qlog/show/%s/' % str(project_log.id)
            return HttpResponseRedirect(url)
    else:
        print('GET')
        dummy_instance = ProjectLog()
        if project.person is not None:
            dummy_instance.technical_lead = project.person
            form = ProjectLogNoProjectFormAsync(instance=dummy_instance, initial={'qa_log_number_x':init_x, 'qa_log_number_y':init_y, 'project': project})
        else:
            form = ProjectLogNoProjectFormAsync(initial={'qa_log_number_x':init_x, 'qa_log_number_y':init_y, 'project': project})
    return render(request, 'main/create_qlog.html', locals())


@login_required
@apply_perms
def edit_project_log(request, project_log_id,**kwargs):
    user = request.user
    profile = user.userprofile
#    project_log = ProjectLog.objects.get(id=project_log_id)
    project_log = get_object_or_404(ProjectLog, id=project_log_id)

    #Dropdown for edit should always include QA Activity lab/center and project lab/center.
    include_labs = [project_log.lab_id, project_log.project.lab_id]
    # get the organization data
    office_list = oq.get_office_list(user, as_json=True)
    lab_list = oq.get_lab_list(user, office=None, as_json=True,include_labs=include_labs)
    division_list = oq.get_division_list(user, None, None, as_json=True)
    branch_list = oq.get_branch_list(user, None, None, None, as_json=True)

    projectlog_update_history = ProjectLog_update_history.objects.filter(project_log=project_log)

    # poc_list_objs = UserProfile.objects.all()

    poc_list_objs = (
        UserProfile.objects
            .select_related("user","office","lab","division","branch")
            .all()
    )

    poc_list = json.dumps([{"id": obj.id, "user_id": obj.user.id, "office_id": obj.office.id if obj.office else 0,
                            "lab_id": obj.lab.id if obj.lab else 0,
                            "division_id": obj.division.id if obj.division else 0,
                            "branch_id": obj.branch.id if obj.branch else 0}
                           for obj in poc_list_objs])

    # formatting for the organization selector
    office_required = True
    lab_required = True
    division_required = True
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    title = "Update QA Activity"

    selected_office = project_log.office;
    selected_lab = project_log.lab;
    selected_division = project_log.division;
    selected_branch = project_log.branch;
    obj = project_log
    project = project_log.project
    project_logs = ProjectLog.objects.filter(project=project)

    # The clone_y value is used in site_base_qlog_show.html to populate the Clone QA Activity action.
    # Right now we're just incrementing, not checking if an activity already exists with the +1 ID.
    # However, QA Track is smart enough to give it the right ID if you actually use the action to clone.
    pl_qa_log_number_type = obj.project_log_type.abbreviation
    pl_qa_log_number_x = obj.qa_log_number_x
    pl_qa_log_number_y = obj.qa_log_number_y
    y_plus_one = int(pl_qa_log_number_y) + 1
    clone_y = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(pl_qa_log_number_x) + '-' + str(y_plus_one)

    the_post_form = ProjectLogFormAsync(data=request.POST, files=request.FILES, instance=project_log)
    the_form = ProjectLogFormAsync(instance=project_log)

    if request.method == "POST":
        form = the_post_form

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        selected_office = Office.objects.get(id = office_id) if oq._valid_org_id(office_id) else None
        selected_lab = Lab.objects.get(id = lab_id) if oq._valid_org_id(lab_id) else None
        selected_division = Division.objects.get(id = division_id) if oq._valid_org_id(division_id) else None
        selected_branch = Branch.objects.get(id = branch_id) if oq._valid_org_id(branch_id) else None

        # These are used for deciding if activity and project update history entries should be created.
        before_date_approved = obj.date_approved
        before_review_type = obj.review_type
        before_technical_lead = obj.technical_lead
        before_reviewer = obj.reviewer
        before_qapp_status = project.qapp_status
        before_qapp_approval_date = project.qapp_approval_date
        before_last_qapp_review_date = project.last_qapp_review_date
        update_comments = request.POST.get("update_comment")

        if form.is_valid():
            project_log = form.save(commit=False)

            if project_log.title == '':
                project_log.title = project.title

            if project_log.date_responses_received == '':
                project_log.date_responses_received = None
            if project_log.date_received == '':
                project_log.date_received = None
            if project_log.date_reviewed == '':
                project_log.date_reviewed = None
            if project_log.date_approved == '':
                project_log.date_approved = None
            if project_log.date_review_requested == '':
                project_log.date_review_requested = None

            project_log.last_modified_by = user.username

            project_log.save()

            # Check if project fields should be updated as a result of a QAPP QA activity update.
            if project_log.project_log_type.the_name == 'QAPP':

                if project_log.date_received is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
                else:
                    pass

                if project_log.date_reviewed is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
                else:
                    pass

                if project_log.date_approved is not None:
                    project.qapp_approval_date = project_log.date_approved
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
                    if project.last_qapp_review_date is not None:
                        if project_log.date_approved > project.last_qapp_review_date:
                            project.last_qapp_review_date = project_log.date_approved
                    else:
                        project.last_qapp_review_date = project_log.date_approved
                else:
                    pass

                project.save()

                # Add entry to project update history if project's fields changed (Only for QAPP QA activities).
                log_hist = False

                if before_qapp_status != project.qapp_status:
                    log_hist = True
                elif before_qapp_approval_date != project.qapp_approval_date:
                    log_hist = True
                elif before_last_qapp_review_date != project.last_qapp_review_date:
                    log_hist = True

                if log_hist:
                    # If user hasn't entered update comment, then add default.
                    if not update_comments:
                        update_comments = 'QAPP QA activity edited'

                    # add to project update history
                    project_update_history = Project_update_history.objects.create(project=project,
                                                                                   user=user,
                                                                                   date_qappreviewed=project.last_qapp_review_date,
                                                                                   projectlead=project.person,
                                                                                   qa_manager=project.qa_manager,
                                                                                   project_status=project.project_status,
                                                                                   qapp_status=project.qapp_status,
                                                                                   comments=update_comments)

            else:
                pass

            # Add entry to QA activity Update History if key fields changed when editing.
            log_hist = False
            if before_date_approved != project_log.date_approved:
                log_hist = True
            elif before_review_type != project_log.review_type:
                log_hist = True
            elif before_technical_lead != project_log.technical_lead:
                log_hist = True
            elif before_reviewer != project_log.reviewer:
                log_hist = True
            elif update_comments:
                log_hist = True

            if log_hist:
                # add entry to QA activity update history
                projectlog_update_history = ProjectLog_update_history.objects.create(project_log=project_log,
                                                                                     user=user,
                                                                                     date_approved=project_log.date_approved,
                                                                                     review_type=project_log.review_type,
                                                                                     technical_lead=project_log.technical_lead,
                                                                                     reviewer=project_log.reviewer,
                                                                                     comments=update_comments)

            url = '/projects/qlog/show/%s/' % str(project_log.id)
            return HttpResponseRedirect(url)
    else:
        form = the_form

    return render(request, 'main/edit_project_log.html', locals())



# Commented out to test it's not in use
# @login_required
# @apply_perms
# def edit_project_log_review(request, project_log_id, **kwargs):
#     user = request.user
#     profile = user.userprofile
#
#     if profile.user_type == "SUPER" or profile.can_edit == "Y":
#         error_message = "You can edit QA Activities and QA Reviews"
#     else:
#         error_message = "You are not authorized to edit QA Activities or QA Reviews."
#         back_link = "/projects/qlog/search/"
#         return render(request, 'error.html', locals())
#
#     title = "Update QA Activity"
#
#     project_log = ProjectLog.objects.get(id=project_log_id)
#     project = project_log.project
#     project_logs = ProjectLog.objects.filter(project=project)
#
#     if profile.user_type == "SUPER" or user == project_log.user:
#         pass
#     else:
#         return render(request, 'no_edit.html', locals())
#
#     if request.method == "POST":
#         form = ProjectLogReviewForm(data=request.POST, files=request.FILES, instance=project_log)
#         if form.is_valid():
#             project_log = form.save(commit=False)
#
#             project_log.last_modified_by = user.username
#             project_log.save()
#
#             url = '/projects/qlog/show/%s/' % str(project_log.id)
#             return HttpResponseRedirect(url)
#     else:
#         form = ProjectLogReviewForm(instance=project_log)
#
#     return render(request, 'main/edit_review.html', locals())

@login_required
@apply_perms
def delete_project_log(request, project_log_id,**kwargs):
    title = "Delete  QA Activity"
    user = request.user
    project_log = get_object_or_404(ProjectLog, id=project_log_id)

    if project_log.user == user:
        project_log.delete()

    url = '/projects/qlog/list/'
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def list_project_logs(request,**kwargs):
    user = request.user
    title = " QA Activity List"
    if labs > 0:
        for l in labs:
            projs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation))
            for p in projs:
                projects.append(p)
                the_count = len(projects)
            projects.sort('the_name')
    if not labs:
        objs = ProjectLog.objects.filter(query & Q(division__lab__abbreviation=lab.abbreviation))
        the_count = ProjectLog.objects.filter(query & Q(division__lab__abbreviation=lab.abbreviation)).count()
        query_show = query_show + " (Center => " + lab.abbreviation + ")"
    project_statuses = ProjectStatus.objects.all().order_by('the_name')
    qapp_statuses = QappStatus.objects.all().order_by('the_name')
    qa_categories = QaCategory.objects.all().order_by('the_name')
    return render(request, 'main/search_project_logs.html', locals())

@login_required
@apply_perms
def pdf_qlog(request, project_log_id, make_pdf_file=0,**kwargs):
    user = request.user

    qlog = ProjectLog.objects.get(id=project_log_id)

    # Make sure we have good values. The Paragraph() call does not like None,
    # so here we check for that fields exist and if they have value None, set it to ''

    try:
        technical_lead_full_name = str(qlog.technical_lead.last_name) + ", " + str(qlog.technical_lead.first_name)
    except:
        technical_lead_full_name = ''

    try:
        technical_lead_org = qlog.technical_lead.userprofile.branch
    except:
        try:
            technical_lead_org = qlog.technical_lead.userprofile.division
        except:
            technical_lead_org = ''

    if qlog.reviewer is not None and qlog.reviewer != '':
        reviewer_full_name = str(qlog.reviewer.last_name) + ", " + str(qlog.reviewer.first_name)
    else:
        reviewer_full_name = ""

    if qlog.title is None:
        qlog.title = ''

    if qlog.qa_review_comment is None:
        qlog.qa_review_comment = ''

    rap_fields = get_rap_fields()

    raps = []
    project = qlog.project
    i = 0
    for rap in rap_fields:
        valString = getattr(project,rap)
        if valString != '' and valString is not None:
            if rap == 'hsrp_rap_extensions':
                program = 'HSRP Extensions'
            else:
                program = rap.split('_')[0].upper()
            valString = str(valString)
            valueList = sort_rap_numbers(re.split(r'; |, |;|,',valString))
            values = ', '.join(valueList)
            if not values.startswith(program):
                values = program + ' ' + values
            if i ==0:
                title = "Rap Numbers:"
            else:
                title = ""
            row = {'title':title, 'values':values}
            raps.append(row)
            i += 1

    # Create checkboxes using rectangle
    checkbox = flowable_rect(6, 6, False)
    checkbox_filled = flowable_rect(6, 6, True)

    checkbox_hisa = checkbox
    checkbox_isi = checkbox
    checkbox_requires_advanced_notification = checkbox
    checkbox_noneoftheabove = checkbox

    try:
        product_category = qlog.product_category_id
    except:
        product_category = 0

    if product_category == 1:
        checkbox_hisa = checkbox_filled
    elif product_category == 2:
        checkbox_isi = checkbox_filled
    elif product_category == 3:
        checkbox_requires_advanced_notification = checkbox_filled
    elif product_category == 4:
        checkbox_noneoftheabove = checkbox_filled

    mark_approved = ''
    mark_approved_minor_revs = ''
    mark_not_approved = ''
    mark_no_approved_qapp_identified = ''
    mark_req_not_applicable = ''
    checkbox_approved = checkbox
    checkbox_approved_minor_revs = checkbox
    checkbox_not_approved = checkbox
    checkbox_no_approved_qapp_identified = checkbox
    checkbox_req_not_applicable = checkbox

    try:
        review_type_final = qlog.review_type.the_name
    except:
        review_type_final = ''

    x_text = '<b><font size=16>X</font></b>'

    if review_type_final == "Approved":
        mark_approved = x_text
        checkbox_approved = checkbox_filled
    elif review_type_final == "Approved with minor revisions":
        mark_approved_minor_revs = x_text
        checkbox_approved_minor_revs = checkbox_filled
    elif review_type_final == "Not Approved revisions required":
        mark_not_approved = x_text
        checkbox_not_approved = checkbox_filled
    elif review_type_final == "No approved QAPP identified":
        mark_no_approved_qapp_identified = x_text
        checkbox_no_approved_qapp_identified = checkbox_filled
    elif review_type_final == "QA requirements are not applicable":
        mark_req_not_applicable = x_text
        checkbox_req_not_applicable = checkbox_filled

    if review_type_final != '':
        header_text = "ORD QA Activity Review Form"
    else:
        header_text = "This QA Review form printout lacks a Review Recommendation and is incomplete."

    response = HttpResponse(content_type='application/pdf')

    my_buffer = settings.MEDIA_ROOT + "%s/qa_reviews/qa_review_%s.pdf" % (str(user.username), str(qlog.qa_log_number))
    my_directory = settings.MEDIA_ROOT + "%s/qa_reviews/" % str(user.username)
    try:
        os.makedirs( my_directory, 0o755 )
    except OSError as e:
        pass

    if make_pdf_file == 0:
        doc = SimpleDocTemplate(response, pagesize=letter,
                                rightMargin=20, leftMargin=10,
                                topMargin=36, bottomMargin=18)
    else:
        doc = SimpleDocTemplate(my_buffer, pagesize=letter,
                                rightMargin=20, leftMargin=10,
                                topMargin=36, bottomMargin=18)

    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=12, leading=14))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, fontSize=10, leading=14, borderPadding=5, leftIndent=5))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontSize=12, leading=14))
    styles.add(ParagraphStyle(name='Inset', alignment=TA_LEFT, fontSize=12, leftIndent=36, leading=14))
    styles.add(ParagraphStyle(name='LeftIndented', alignment=TA_LEFT, fontSize=10, leading=12, borderPadding=0, leftIndent=10))
    styles.add(ParagraphStyle(name='Footnote', alignment=TA_LEFT, fontSize=8, leading=10, borderPadding=0, leftIndent=10))

    elements.append(Paragraph(header_text, styles["Center"]))
    elements.append(Spacer(1, 12))

    table_product_information_header = Table([[Paragraph("QA ACTIVITY INFORMATION", styles["Center"])]])
    table_product_information_header.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                 ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                 ('BACKGROUND', (1, 1), (-2, -2), whitesmoke),
                                  ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                  ('BOX', (0, 0), (-1, -1), 0.25, black)
                                  ]))
    elements.append(table_product_information_header)

    # Product Category checkbox table
    # Default is none checked
    hisa_str = "HISA (Highly Influential Scientific Assessment)"
    isi_str = "ISI (Influential Scientific Information)"
    requires_advanced_notification_str = "Requires advance Notification (Not HISA or ISI)"
    noneoftheabove_str = "None of the above"
    table_productcategory = Table([[checkbox_hisa, Paragraph(hisa_str, styles["LeftIndented"])],
                             [checkbox_isi, Paragraph(isi_str, styles["LeftIndented"])],
                             [checkbox_requires_advanced_notification, Paragraph(requires_advanced_notification_str, styles["LeftIndented"])],
                             [checkbox_noneoftheabove, Paragraph(noneoftheabove_str, styles["LeftIndented"])]
                             ], colWidths=[10, 250], hAlign="LEFT")
    table_productcategory.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                          ('LEFTPADDING', (0, 0), (-1, -1), 5)]))


    qapp_numbers = ""
    if qlog.qapp:
        qapp_numbers = qlog.qapp.qa_log_number

    # QA Category checkbox table
    # Default is neither checked
    table_qacategory = Table([[checkbox, "A"], [checkbox, "B"], [checkbox, "Not Applicable"]], colWidths=[10, 200], hAlign="LEFT")
    if qlog.project.qa_category:
        if qlog.project.qa_category.the_name == "A" or qlog.project.qa_category.the_name == "I" or qlog.project.qa_category.the_name == "II": # Check A
            table_qacategory = Table([[checkbox_filled, "A"], [checkbox, "B"], [checkbox, "Not Applicable"]], colWidths=[10, 200], hAlign="LEFT")
        elif qlog.project.qa_category.the_name == "B" or qlog.project.qa_category.the_name == "III" or qlog.project.qa_category.the_name == "IV": # Check B
            table_qacategory = Table([[checkbox, "A"], [checkbox_filled, "B"], [checkbox, "Not Applicable"]], colWidths=[10, 200], hAlign="LEFT")
        else:
            table_qacategory = Table([[checkbox, "A"], [checkbox, "B"], [checkbox_filled, "Not Applicable"]], colWidths=[10, 200], hAlign="LEFT")
    table_qacategory.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                 ('LEFTPADDING', (0, 0), (-1, -1), 5)]))

    table_data = []
    # add rows here
    # IMPORTANT:
    # If you add new fields to the PDF, and those fields may have a value of None,
    # you MUST add a check above for the None value and set it to ''
    # otherwise the app will crash on the Paragraph() call below.

    for rap in raps:
        table_data.append([Paragraph("<b>RAP Project/Task ID:</b>", styles["Left"]), Paragraph(rap['values'], styles["Left"])])

    table_data.append([Paragraph("<b>QA Activity Number:</b>", styles["Left"]), Paragraph(qlog.qa_log_number, styles["Left"])])
    table_data.append([Paragraph("<b>Scientific/Technical Product or QA Document Title:</b>", styles["Left"]), Paragraph(qlog.title, styles["Left"])])

    table_data.append([Paragraph("<b>QA Activity Type<sup>1</sup> / Sub-Type<sup>2</sup>:</b>", styles["Left"]), Paragraph(qlog.project_log_type.the_name, styles["Left"])])
    table_data.append([Paragraph("<b>QA Activity Contact / Organization:</b>", styles["Left"]), Paragraph(technical_lead_full_name + " / " + str(technical_lead_org), styles["Left"])])

    if qlog.lco_tracking_number:
        table_data.append([Paragraph("<b>STICS Clearance Tracking Number (if applicable):</b>", styles["Left"]), Paragraph(str(qlog.lco_tracking_number), styles["Left"])])
    table_data.append([Paragraph("<b>Product Category:</b>", styles["Left"]), table_productcategory])

    # Only include latest QAPP number if not activity being reviewed is not a QAPP
    if qlog.project_log_type.the_name != "QAPP":
        table_data.append([Paragraph("<b>QAPP QA Activity Number<sup>3</sup>:</b>", styles["Left"]), Paragraph(qapp_numbers, styles["Left"])])

    table_data.append([Paragraph("<b>QA Category:</b>", styles["Left"]), table_qacategory])

    # Create the table
    user_table = Table(table_data)
    user_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                    ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                    ('BOX', (0, 0), (-1, -1), 0.25, black)
                                    ]))
    elements.append(user_table)

    table_product_information_header = Table([[Paragraph("QA REVIEW REPORT", styles["Center"])]])
    table_product_information_header.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                                          ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                                          ('BACKGROUND', (1, 1), (-2, -2), whitesmoke),
                                                          ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                                          ('BOX', (0, 0), (-1, -1), 0.25, black)
                                                          ]))
    elements.append(table_product_information_header)

    table_qam_date = Table([[Paragraph("<b>QA Manager (QAM) or Designee:</b> " + reviewer_full_name, styles["Left"])],
                            [Paragraph("<b>Date QA Document / Product Received by QAM:</b> " + str(
                                qlog.date_received), styles["Left"])]
                            ])
    table_qam_date.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, black)
                                        ]))
    elements.append(table_qam_date)

    approved_str = "<b>Approved</b> - Approved QAPP<sup>4</sup> identified for the product. If the product was reviewed, no deficiencies<sup>5</sup> were identified in the product."
    approved_minor_revs_str = "<b>Approved with Minor Revisions</b> - Approved QAPP identified for the product. If the product was reviewed, observations<sup>6</sup> were identified in the product that should be addressed, but no additional QA review is required."
    not_approved_str = "<b>Not Approved</b> - Approved QAPP identified for the product. Findings<sup>7</sup> were identified in the product that require corrective action. A response to each finding, along with corrected text, must be provided for additional QA review."
    no_approved_qapp_identified_str = "<b>No approved QAPP was identified for the product</b>"
    not_applicable_str = "<b>QA requirements are not applicable to this product</b>"

    # Review Recommendation checkbox table
    table_reviewrec = Table([[checkbox_approved, Paragraph(approved_str, styles["LeftIndented"])],
                             [checkbox_approved_minor_revs, Paragraph(approved_minor_revs_str, styles["LeftIndented"])],
                             [checkbox_not_approved, Paragraph(not_approved_str, styles["LeftIndented"])],
                             [checkbox_no_approved_qapp_identified, Paragraph(no_approved_qapp_identified_str, styles["LeftIndented"])],
                             [checkbox_req_not_applicable, Paragraph(not_applicable_str, styles["LeftIndented"])]
                             ], colWidths=[10, 530], hAlign="LEFT")
    table_reviewrec.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 5)]))

    table2 = Table([[table_reviewrec]])
    table2.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('LEFTPADDING', (0, 0), (-1, -1), 20),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, black)
                                        ]))
    elements.append(table2)

    table_comments = Table([[Paragraph("<b>Comments:</b><br/>" + str(qlog.qa_review_comment), styles["Left"])],
                            [Paragraph("<b>QA Manager or Designee Signature & Date:</b> " + reviewer_full_name + " " + str(qlog.date_reviewed), styles["Left"])]
                            ])
    table_comments.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                                          ('LEFTPADDING', (0, 0), (-1, -1), 5),
                                                          ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
                                                          ('BOX', (0, 0), (-1, -1), 0.25, black)
                                                          ]))
    elements.append(table_comments)

    elements.append(Spacer(1, 6))

    footnote1 = "<b><sup>1</sup>QA Activity Type:</b> Note that posters, presentations, and abstracts do NOT require a QA review."
    footnote2 = "<b><sup>2</sup>QA Activity Type (Sub-Type):</b> Book, Book Chapter, Internal Report, EPA Published Proceedings, Paper in EPA Proceedings, Non-EPA Published Proceedings, Paper in Non-EPA Proceedings, Newsletter, Unpublished Report, Data (Database, Map, Model, Scientific Data, Software, Spreadhseet), Journal Article (Non-Peer Reviewed, Peer Reviewed), Abstract, Presentation (Poster, Slide), Published Report (Guidance Document, Handbook, Issue Paper, Manual, Methodology, Report (default), Technology Transfer, User's Guide)"
    footnote3 = "<b><sup>3</sup>QAPP QA Activity Number:</b> The QA activity number for the project QAPP that applies to this product. See Comments for other relevant QAPPs."
    footnote4 = "<b><sup>4</sup>QAPP:</b> Specific QA project planning documentation developed and approved prior to (a) the collection, evaluation, use (including use of non-EPA collected data or research [i.e., existing data] such as results from literature searches), generation, or reporting of environmental data by or for EPA, or (b) the design, construction, and operation of environmental technology by EPA (including software, models, and methods) for environmental programs as identified in <a href=\"https://www.epa.gov/sites/production/files/2015-09/documents/epa_order_cio_21050.pdf\"><u>EPA CIO Order 2105.0</u></a>, Section 5, <i>Scope and Field of Application</i>."
    footnote5 = "<b><sup>5</sup>Deficiency:</b> Unauthorized deviation from acceptable procedures or practices, or a defect in an item."
    footnote6 = "<b><sup>6</sup>Observation:</b> Assessment conclusion that identifies a deficiency which has the potential to have a significant impact on an item or activity. An observation may identify a deficiency which does not yet cause a degradation in quality."
    footnote7 = "<b><sup>7</sup>Finding:</b> Assessment conclusion that identifies a deficiency having a significant effect on an item or activity."

    elements.append(Paragraph(footnote1, styles["Footnote"]))
    elements.append(Paragraph(footnote2, styles["Footnote"]))
    # Only include latest QAPP number if not activity being reviewed is not a QAPP
    if qlog.project_log_type.the_name != "QAPP":
        elements.append(Paragraph(footnote3, styles["Footnote"]))
    elements.append(Paragraph(footnote4, styles["Footnote"]))
    elements.append(Paragraph(footnote5, styles["Footnote"]))
    elements.append(Paragraph(footnote6, styles["Footnote"]))
    elements.append(Paragraph(footnote7, styles["Footnote"]))

    doc.build(elements)

    qlog.attachment_pdf = "%s/qa_reviews/qa_review_%s.pdf" % (str(user.username), str(qlog.qa_log_number))
    qlog.save()

    return response


@login_required
@never_cache
@apply_perms
def show_project_log(request, project_log_id,**kwargs):
    user = request.user

    expand_files = False

    obj = get_object_or_404(ProjectLog, id=project_log_id)
    project = obj.project
    qa_review_distribution_list = obj.qa_review_distribution_list.all()
    projectlog_update_history = ProjectLog_update_history.objects.filter(project_log=obj)

    # Parse weblink to handle multiple links.
    if obj.weblink:
        weblinks_list = obj.weblink.split(' ')
        # Remove any blank entries created by multiple spaces in a row.
        for link in weblinks_list:
            if link == '':
                weblinks_list.remove('')

    pl_qa_log_number_type = obj.project_log_type.abbreviation
    pl_qa_log_number_x = obj.qa_log_number_x
    pl_qa_log_number_y = obj.qa_log_number_y

    x_plus_one = int(pl_qa_log_number_x) + 1
    y_plus_one = int(pl_qa_log_number_y) + 1
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) &
                                                    Q(project_log_type__the_name='QAPP')).count()
    title = "Show QA Activity"
    if obj.project_log_type.the_name == 'QAPP':
        is_not_qapp = False
    else:
        is_not_qapp = True

    if obj.review_type is not None or obj.qa_review_comment is not None:
        has_review = True
    else:
        has_review = False

    clone_x = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(x_plus_one) + '-' + str(0)
    clone_y = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(pl_qa_log_number_x) + '-' + str(y_plus_one)

    clone_x_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)
    clone_y_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)

    qlogs = ProjectLog.objects.filter(project=project)
    the_count = ProjectLog.objects.filter(project=project).count()
    project_attachments = ProjectAttachment.objects.filter(project_log=obj)

    # If the QA Activity is the latest EP or any QAPP and the project has restricted either of those then
    # we have to figure out the eligable users.
    latest_ep_qlog = get_latest_ep(ProjectLog.objects.filter(Q(project_id=obj.project_id) & Q(project_log_type__the_name='Extramural Package')))

    if obj == latest_ep_qlog or obj.project_log_type.the_name == 'QAPP':

        eligable_users = get_project_users(qlog=obj)
        if kwargs["allow_edit"]:
            eligable_users.append(user)

        for att in project_attachments:

            if obj == latest_ep_qlog and obj.project.restrict_ext_package_files and user not in eligable_users:
                att.restricted = True
                att.restricted_ep = True

            if obj.project_log_type.the_name == 'QAPP' and obj.project.restrict_qapp_files and user not in eligable_users:
                    att.restricted = True
                    att.restricted_qapp = True

    return render(request, 'show/show_project_log.html', locals())


@login_required
@never_cache
@apply_perms
def show_project_log_expanded(request, project_log_id,**kwargs):
    user = request.user

    expand_files = True

    obj = get_object_or_404(ProjectLog, id=project_log_id)
    project = obj.project
    qa_review_distribution_list = obj.qa_review_distribution_list.all()
    projectlog_update_history = ProjectLog_update_history.objects.filter(project_log=obj)

    # Parse weblink to handle multiple links.
    if obj.weblink:
        weblinks_list = obj.weblink.split(' ')
        # Remove any blank entries created by multiple spaces in a row.
        for link in weblinks_list:
            if link == '':
                weblinks_list.remove('')

    pl_qa_log_number_type = obj.project_log_type.abbreviation
    pl_qa_log_number_x = obj.qa_log_number_x
    pl_qa_log_number_y = obj.qa_log_number_y

    x_plus_one = int(pl_qa_log_number_x) + 1
    y_plus_one = int(pl_qa_log_number_y) + 1
    project_qapps_count = ProjectLog.objects.filter(Q(project=project) &
                                                    Q(project_log_type__the_name='QAPP')).count()
    title = "Show QA Activity"
    if obj.project_log_type.the_name == 'QAPP':
        is_not_qapp = False
    else:
        is_not_qapp = True

    if obj.review_type is not None or obj.qa_review_comment is not None:
        has_review = True
    else:
        has_review = False

    clone_x = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(x_plus_one) + '-' + str(0)
    clone_y = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(pl_qa_log_number_x) + '-' + str(y_plus_one)

    clone_x_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)
    clone_y_qapp = project.qa_id + '-' + pl_qa_log_number_type + '-' + str(1) + '-' + str(project_qapps_count)

    qlogs = ProjectLog.objects.filter(project=project)
    the_count = ProjectLog.objects.filter(project=project).count()
    project_attachments = ProjectAttachment.objects.filter(project_log=obj)

    # If the QA Activity is the latest EP or any QAPP and the project has restricted either of those then
    # we have to figure out the eligable users.
    latest_ep_qlog = get_latest_ep(ProjectLog.objects.filter(Q(project_id=obj.project_id) & Q(project_log_type__the_name='Extramural Package')))

    if obj == latest_ep_qlog or obj.project_log_type.the_name == 'QAPP':

        eligable_users = get_project_users(qlog=obj)
        if kwargs["allow_edit"]:
            eligable_users.append(user)

        for att in project_attachments:

            if obj == latest_ep_qlog and obj.project.restrict_ext_package_files and user not in eligable_users:
                att.restricted = True
                att.restricted_ep = True

            if obj.project_log_type.the_name == 'QAPP' and obj.project.restrict_qapp_files and user not in eligable_users:
                    att.restricted = True
                    att.restricted_qapp = True

    return render(request, 'show/show_project_log.html', locals())


@login_required
@apply_perms
def excel_project_logs(request, project_log_id,**kwargs):
    user = request.user
    obj = get_object_or_404(ProjectLog, id=project_log_id)
    title = "Show QA Activity"
    project = obj.project

    qlogs = ProjectLog.objects.filter(project=project)
    the_count = ProjectLog.objects.filter(project=project).count()

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=qlogs_for_%s.xls' % project.qa_id
    wb = xlwt.Workbook()
    styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
              'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
              'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
              'default': xlwt.Style.default_style}

    sheet = wb.add_sheet('QLog')
    sheet.write(0, 0, 'Division')
    sheet.write(0, 1, 'Branch')
    sheet.write(0, 2, 'Project Lead First')
    sheet.write(0, 3, 'Project Lead Last')
    sheet.write(0, 4, 'QLog Project Lead First')
    sheet.write(0, 5, 'QLog Project Lead Last')
    sheet.write(0, 6, 'Reviewer First')
    sheet.write(0, 7, 'Reviewer Last')
    sheet.write(0, 8, 'Type')
    sheet.write(0, 9, 'Received')
    sheet.write(0, 10, 'Reviewed')
    sheet.write(0, 11, 'Approved')
    sheet.write(0, 12, 'Title')
    sheet.write(0, 13, 'Project')
    i = 1
    for obj in qlogs:

        if obj.division is not None:
            sheet.write(i, 0, obj.division.abbreviation)
        else:
            sheet.write(i, 0, '')

        if obj.branch is not None:
            sheet.write(i, 1, obj.branch.abbreviation)
        else:
            sheet.write(i, 1, '')

        if obj.project.person is not None:
            sheet.write(i, 2, obj.project.person.first_name)
            sheet.write(i, 3, obj.project.person.last_name)
        else:
            sheet.write(i, 2, '')
            sheet.write(i, 3, '')

        if obj.technical_lead is not None:
            sheet.write(i, 4, obj.technical_lead.first_name)
            sheet.write(i, 5, obj.technical_lead.last_name)
        else:
            sheet.write(i, 4, '')
            sheet.write(i, 5, '')

        if obj.reviewer is not None:
            sheet.write(i, 6, obj.reviewer.first_name)
            sheet.write(i, 7, obj.reviewer.last_name)
        else:
            sheet.write(i, 6, '')
            sheet.write(i, 7, '')

        if obj.project_log_type is not None:
            sheet.write(i, 8, obj.project_log_type.the_name)
        else:
            sheet.write(i, 8, '')

        sheet.write(i, 9, obj.date_received, style=styles["date"])
        sheet.write(i, 10, obj.date_reviewed, style=styles["date"])
        sheet.write(i, 11, obj.date_approved, style=styles["date"])
        sheet.write(i, 12, obj.title)

        if obj.project is not None:
            sheet.write(i, 13, obj.project.qa_id)
        else:
            sheet.write(i, 13, '')

        i += 1
    wb.save(response)
    return response

@login_required
@apply_perms
def search_project_log(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    title = "Search For QA Activities - With Results Shown"
    project_log_types = ProjectLogType.objects.all().order_by('the_name')
    product_category_types = ProductCategory.objects.all().order_by('sort_number')
    review_types = ReviewType.objects.all().order_by('the_name')

    # Pass this to populate the QA Review Required? field
    YN_CHOICES_LIST = YN_CHOICES

    return render(request, 'main/search_project_logs.html', locals())

@login_required
@apply_perms
def result_search_project_log(request,**kwargs):
    user = request.user

    query = Q()
    query_show = ''
    the_count = 0

    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id = office_id)
        query = query & (Q(office__id=office_id))
        query_show = query_show + "Office = " + str(office.abbreviation) + ", "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id = lab_id)
        query = query & (Q(lab__id=lab_id))
        query_show = query_show + "Center = " + str(lab.abbreviation) + ", "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id = division_id)
        query = query & (Q(division__id=division_id))
        query_show = query_show + "Division = " + str(division.abbreviation) + ", "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id = branch_id)
        query = query & (Q(branch__id=branch_id))
        query_show = query_show + "Branch = " + str(branch.abbreviation) + ", "

    title = "Search For QA Activities - With Results Shown"
    project_log_types = ProjectLogType.objects.all().order_by('the_name')

    if request is None:
        return ProjectLog.objects.get(id=1)

    if 'kw' in request.GET:
        kw = request.GET['kw']
        if kw:
            query = query & (Q(program__the_name__icontains=kw))
            query_show = query_show + "Keyword contains " + str(kw) + ", "

    if 'qa_activity_id' in request.GET:
        qa_activity_id = request.GET['qa_activity_id']
        qa_activity_id = qa_activity_id.strip()  # Trim white space
        if qa_activity_id:
            query = query & (Q(qa_log_number__icontains=qa_activity_id))
            query_show = query_show + "QA Activity ID contains " + str(qa_activity_id) + ", "

    if 'alt_id' in request.GET:
        alt_id = request.GET['alt_id']
        alt_id = alt_id.strip()  # Trim white space
        if alt_id:
            query = query & (Q(alt_id__icontains=alt_id))
            query_show = query_show + "Alternate ID contains " + str(alt_id) + ", "

    if 'previous_id' in request.GET:
        previous_id = request.GET['previous_id']
        previous_id = previous_id.strip()  # Trim white space
        if previous_id:
            query = query & (Q(previous_id__icontains=previous_id))
            query_show = query_show + "Previous ID contains " + str(previous_id) + ", "

    if 'c' in request.GET:
        c = request.GET['c']
        if c:
            query = query & (Q(technical_lead__last_name__istartswith=c))
            query_show = query_show + "QA Activity POC Last Name starts with " + str(c) + ", "

    if 'fn' in request.GET:
        fn = request.GET['fn']
        if fn:
            query = query & (Q(technical_lead__first_name__istartswith=fn))
            query_show = query_show + "QA Activity POC First Name starts with " + str(fn) + ", "

    if 't' in request.GET:
        t = request.GET['t']
        if t:
            query = query & (Q(project__person__last_name__istartswith=t))
            query_show = query_show + "Project Lead Last Name starts with " + str(t) + ", "

    if 'v' in request.GET:
        v = request.GET['v']
        if v:
            query = query & (Q(project__person__first_name__istartswith=v))
            query_show = query_show + "Project Lead First Name starts with " + str(v) + ", "

    if 'e' in request.GET:
        e = request.GET['e']
        if e:
            query = query & (Q(reviewer__last_name__istartswith=e))
            query_show = query_show + "Reviewer Last Name starts with " + str(e) + ", "

    if 'f' in request.GET:
        f = request.GET['f']
        if f:
            query = query & (Q(reviewer__first_name__istartswith=f))
            query_show = query_show + "Reviewer First Name starts with " + str(f) + ", "

    item_01 = ''
    sub_query_01 = Q()
    sub_query_show_01 = ''
    if 'r' in request.GET:
        r = request.GET.getlist('r')
        if r:
            for item_01 in r:
                sub_query_01 = sub_query_01 | Q(project_log_type__the_name__iexact=item_01)
                sub_query_show_01 = sub_query_show_01 + str(item_01) + ", "

            query = sub_query_01 & query
            query_show = query_show + "QA Activity Type(s) => " + sub_query_show_01

    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'product_categories' in request.GET:
        product_categories = request.GET.getlist('product_categories')
        if product_categories:
            for item_03 in product_categories:
                sub_query_03 = sub_query_03 | Q(product_category__the_name__iexact=item_03)
                sub_query_show_03 = sub_query_show_03 + str(item_03) + ", "

            query = sub_query_03 & query
            query_show = query_show + "Product Category(ies) => " + sub_query_show_03

    item_02 = ''
    sub_query_02 = Q()
    sub_query_show_02 = ''
    if 'rt' in request.GET:
        rt = request.GET.getlist('rt')
        if rt:
            for item_02 in rt:
                sub_query_02 = sub_query_02 | Q(review_type__the_name__iexact=item_02)
                sub_query_show_02 = sub_query_show_02 + str(item_02) + ", "

            query = sub_query_02 & query
            query_show = query_show + "Review Recommendation(s) => " + sub_query_show_02

    if 'qa_review_required' in request.GET:
        qa_review_required = request.GET['qa_review_required']
        if qa_review_required:
            query = query & (Q(qa_review_required__iexact = qa_review_required))
            query_show = query_show + "Review Required = " + str(qa_review_required) + ", "

    if 'g' in request.GET:
        g = request.GET['g']
        if g:
            query = query & (Q(date_received__gte=g))
            query_show = query_show + "QA Activity Received From Date = " + str(g) + ", "

    if 'dh' in request.GET:
        dh = request.GET['dh']
        if dh:
            query = query & (Q(date_received__lte=dh))
            query_show = query_show + "QA Activity Received To Date = " + str(dh) + ", "

    if 'j' in request.GET:
        j = request.GET['j']
        if j:
            query = query & (Q(date_reviewed__gte=j))
            query_show = query_show + "QA Activity Reviewed From Date = " + str(j) + ", "

    if 'k' in request.GET:
        k = request.GET['k']
        if k:
            query = query & (Q(date_reviewed__lte=k))
            query_show = query_show + "QA Activity Reviewed To Date = " + str(k) + ", "

    if 'm' in request.GET:
        m = request.GET['m']
        if m:
            query = query & (Q(date_approved__gte=m))
            query_show = query_show + "QA Activity Approved From Date = " + str(m) + ", "

    if 'n' in request.GET:
        n = request.GET['n']
        if n:
            query = query & (Q(date_approved__lte=n))
            query_show = query_show + "QA Activity Approved To Date = " + str(n) + ", "

    if 'tl' in request.GET:
        tl = request.GET['tl']
        if tl:
            query = query & (Q(title__icontains=tl))
            query_show = query_show + "Title contains " + str(tl) + ", "

    if 'project_qa_id' in request.GET:
        project_qa_id = request.GET['project_qa_id']
        project_qa_id = project_qa_id.strip()  # Trim white space
        if project_qa_id:
            query = query & (Q(project__qa_id__icontains=project_qa_id))
            query_show = query_show + "Project QA ID contains " + str(project_qa_id) + ", "

    if 'lco_tracking_number' in request.GET:
        lco_tracking_number = request.GET['lco_tracking_number']
        lco_tracking_number = lco_tracking_number.strip()  # Trim white space
        if lco_tracking_number:
            query = query & (Q(lco_tracking_number__icontains=lco_tracking_number))
            query_show = query_show + "STICS Clearance Tracking Number contains " + str(lco_tracking_number) + ", "

    if 'comments' in request.GET:
        comments = request.GET['comments']
        if comments:
            query = query & (Q(the_description__icontains=comments))
            query_show = query_show + "Comments contain \"" + str(comments) + "\""

    objs = ProjectLog.objects.filter(query).all()
    the_count = len(objs)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    rap_fields = get_rap_fields()

    for obj in objs:
        obj.rap = []
        project = obj.project
        for rap in rap_fields:
            valString = getattr(project,rap)
            if valString != '' and valString is not None:
                valString = str(valString)
                if rap == 'hsrp_rap_extensions':
                    program = 'HSRP Extensions'
                else:
                    program = rap.split('_')[0].upper()
                spl = rap.split('_')
                title = spl[0].upper() + ' ' + spl[2].title() + 's:'
                valueList = sort_rap_numbers(re.split(r'; |, |;|,',valString))
                values = ', '.join(valueList)
                if not values.startswith(program):
                    values = program + ' ' + values
                row = {'values':values}
                obj.rap.append(row)

    if 'excel' in request.GET:
        excel = request.GET['excel']
        if excel == "Y":
            qa_activities = objs
            the_count = ProjectLog.objects.filter(query).count()

            response = HttpResponse(content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=qa_activities_searched.xls'
            wb = xlwt.Workbook()
            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            sheet = wb.add_sheet('QA Activities')
            sheet.write(0, 0, 'Division')
            sheet.write(0, 1, 'Branch')
            sheet.write(0, 2, 'Project')
            sheet.write(0, 3, 'Project QA ID')

            sheet.write(0, 4, 'QA Activity')
            sheet.write(0, 5, 'QA Activity ID')
            sheet.write(0, 6, 'Previous ID')
            sheet.write(0, 7, 'Alternate ID')
            sheet.write(0, 8, 'Title')
            sheet.write(0, 9, 'Project Lead First')

            sheet.write(0, 10, 'Project Lead Last')
            sheet.write(0, 11, 'QA Activity POC First')
            sheet.write(0, 12, 'QA Activity POC Last')
            sheet.write(0, 13, 'Reviewer First')

            sheet.write(0, 14, 'Reviewer Last')

            sheet.write(0, 20, 'Recommendation')
            sheet.write(0, 21, 'Date Received')

            sheet.write(0, 22, 'Date Reviewed')
            sheet.write(0, 23, 'Date Approved')
            sheet.write(0, 24, 'STICS Clearance Tracking Number')
            sheet.write(0, 25, 'Product Category')

            sheet.write(0, 26, 'Organization')
            sheet.write(0, 27, 'Number of Findings')
            sheet.write(0, 28, 'All Findings Resolved')
            sheet.write(0, 29, 'Review Required')
            sheet.write(0, 30, 'QAPP QA Activity Number')

            sheet.write(0, 31, 'Review Recommendation')
            sheet.write(0, 32, 'Review Date')
            sheet.write(0, 33, 'Review Email List')
            sheet.write(0, 34, 'Review Comments')

            sheet.write(0, 35, 'QA Activity Comments')
            i = 1
            for obj in qa_activities:
                if obj.division is not None:
                    sheet.write(i, 0, obj.division.abbreviation)
                else:
                    sheet.write(i, 0, '')

                if obj.branch is not None:
                    sheet.write(i, 1, obj.branch.abbreviation)
                else:
                    sheet.write(i, 1, '')

                if obj.project is not None:
                    sheet.write(i, 2, obj.project.title)
                    sheet.write(i, 3, obj.project.qa_id)
                else:
                    sheet.write(i, 2, '')
                    sheet.write(i, 3, '')

                if obj.project_log_type is not None:
                    sheet.write(i, 4, obj.project_log_type.the_name)
                else:
                    sheet.write(i, 4, '')

                sheet.write(i, 5, obj.qa_log_number)
                sheet.write(i, 6, obj.previous_id)
                sheet.write(i, 7, obj.alt_id)
                sheet.write(i, 8, obj.title)

                if obj.project.person is not None:
                    sheet.write(i, 9, obj.project.person.first_name)
                    sheet.write(i, 10, obj.project.person.last_name)
                else:
                    sheet.write(i, 9, '')
                    sheet.write(i, 10, '')

                if obj.technical_lead is not None:
                    sheet.write(i, 11, obj.technical_lead.first_name)
                    sheet.write(i, 12, obj.technical_lead.last_name)
                else:
                    sheet.write(i, 11, '')
                    sheet.write(i, 12, '')

                if obj.reviewer is not None:
                    sheet.write(i, 13, obj.reviewer.first_name)
                    sheet.write(i, 14, obj.reviewer.last_name)
                else:
                    sheet.write(i, 13, '')
                    sheet.write(i, 14, '')

                sheet.write(i, 20, obj.recommendation)
                sheet.write(i, 21, obj.date_received, style=styles["date"])

                sheet.write(i, 22, obj.date_reviewed, style=styles["date"])
                sheet.write(i, 23, obj.date_approved, style=styles["date"])
                sheet.write(i, 24, obj.lco_tracking_number)

                if obj.product_category is not None:
                    sheet.write(i, 25, obj.product_category.the_name)
                else:
                    sheet.write(i, 25, '')

                sheet.write(i, 26, obj.organization)
                sheet.write(i, 27, obj.number_of_finding)
                sheet.write(i, 28, obj.is_finding_resolved)
                sheet.write(i, 29, obj.qa_review_required)

                if obj.qapp is not None:
                    sheet.write(i, 30, obj.qapp.qa_log_number)
                else:
                    sheet.write(i, 30, '')

                if obj.review_type is not None:
                    sheet.write(i, 31, obj.review_type.the_name)
                else:
                    sheet.write(i, 31, '')

                sheet.write(i, 32, obj.qa_review_date, style=styles["date"])
                sheet.write(i, 33, obj.qa_review_email_list)
                sheet.write(i, 34, obj.qa_review_comment)

                sheet.write(i, 35, obj.the_description)
                i += 1
            sheet1 = wb.add_sheet('Query')
            sheet1.write(1, 0, query_show)

            wb.save(response)
            return response

    return render(request, 'main/search_project_log_result.html', locals())

# @login_required
# @apply_perms
# def search_project_logs_for_last_30(request,**kwargs):
#     user = request.user
#
#     query = Q()
#     query_show = 'QA Activities Received For Last 30 Days'
#     project_log_types = ProjectLogType.objects.all().order_by('the_name')
#
#     title = "QA Activities Received Last 30 Days - With Results Shown"
#     d = datetime.today() - timedelta(days=30)
#     query = Q(date_received__gte=d)
#
#
#     objs = []
#     labs = get_labs(user)
#     lab = get_lab(user)
#     if labs > 0:
#         for l in labs:
#             projs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation) & Q(date_received__gte=d))
#             for p in projs:
#                 objs.append(p)
#                 the_count = len(objs)
#     if not labs:
#         objs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d))
#         the_count = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d)).count()
#
#     return render(request, 'main/search_project_logs.html', locals())
#
# @login_required
# @apply_perms
# def search_project_logs_for_last_60(request,**kwargs):
#     user = request.user
#     query = Q()
#     query_show = 'QA Activities Received For Last 60 Days'
#     project_log_types = ProjectLogType.objects.all().order_by('the_name')
#
#     title = "QA Activities Received Last 60 Days"
#     d = datetime.today() - timedelta(days=60)
#
#     objs = []
#     labs = get_labs(user)
#     lab = get_lab(user)
#     if labs > 0:
#         for l in labs:
#             projs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation) & Q(date_received__gte=d))
#             for p in projs:
#                 objs.append(p)
#                 the_count = len(objs)
#     if not labs:
#         objs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d))
#         the_count = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d)).count()
#
#     return render(request, 'main/search_project_logs.html', locals())
#
# @login_required
# @apply_perms
# def search_project_logs_for_last_90(request,**kwargs):
#     user = request.user
#     query = Q()
#     query_show = 'QA Activities Received For Last 90 Days'
#     project_log_types = ProjectLogType.objects.all().order_by('the_name')
#
#     title = "QA Activities Received Last 90 Days - With Results Shown"
#     d = datetime.today() - timedelta(days=90)
#
#     objs = []
#     labs = get_labs(user)
#     lab = get_lab(user)
#     if labs > 0:
#         for l in labs:
#             projs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation) & Q(date_received__gte=d))
#             for p in projs:
#                 objs.append(p)
#                 the_count = len(objs)
#     if not labs:
#         objs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d))
#         the_count = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d)).count()
#
#     return render(request, 'main/search_project_logs.html', locals())
#
# @login_required
# @apply_perms
# def search_project_logs_for_last_180(request,**kwargs):
#     user = request.user
#     query = Q()
#     query_show = 'QA Activities Received For Last 180 Days'
#     project_log_types = ProjectLogType.objects.all().order_by('the_name')
#
#     title = "QA Activities Received Last 180 Days - With Results Shown"
#     d = datetime.today() - timedelta(days=180)
#
#     objs = []
#     labs = get_labs(user)
#     lab = get_lab(user)
#     if labs > 0:
#         for l in labs:
#             projs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=l.abbreviation) & Q(date_received__gte=d))
#             for p in projs:
#                 objs.append(p)
#                 the_count = len(objs)
#     if not labs:
#         objs = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d))
#         the_count = ProjectLog.objects.filter(Q(division__lab__abbreviation__exact=lab.abbreviation) & Q(date_received__gte=d)).count()
#
#     return render(request, 'main/search_project_logs.html', locals())

####################################################################### End QA Activity





########################################################################## Start Program

@login_required
@apply_perms
def create_program(request,**kwargs):
    user = request.user
    profile = user.userprofile
    title = "Create a New Program"
    programs = Program.objects.all()

    if request.method == "POST":
        form = ProgramForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            program = form.save(commit=False)

            program.user = user
            program.created_by = user.username
            program.last_modified_by = user.username
            program.save()

            url = '/projects/program/show/%s/' % str(program.id)
            return HttpResponseRedirect(url)
    else:
        form = ProgramForm()
    return render(request, 'main/create_program.html', locals())

@login_required
@apply_perms
def edit_program(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile

    title = "Update Program"

    program = Program.objects.get(id=obj_id)
    programs = Program.objects.all()

    if request.method == "POST":
        form = ProgramForm(data=request.POST, files=request.FILES, instance=program)
        if form.is_valid():
            program = form.save(commit=False)

            program.last_modified_by = user.username
            program.save()

            url = '/projects/program/show/%s/' % str(program.id)
            return HttpResponseRedirect(url)
    else:
        form = ProgramForm(instance=program)

    return render(request, 'main/edit_program.html', locals())




@login_required
@never_cache
@apply_perms
def show_program(request, obj_id,**kwargs):
    """
    display detailed view of a program
    :param request:
    :param obj_id:
    :return:
    """
    user = request.user

    program = get_object_or_404(Program, id=obj_id)
    form = ProgramForm(instance=program, read_only=True)

    project_list = Project.objects.filter(programs=program).extra( select={'lower_name': 'lower(title)'}).order_by('lower_name')

    return render(request, 'show/show_project_program.html', locals())

@apply_perms
def search_program(request,**kwargs):
    """
    displays the search page for programs
    :param request:
    :return:
    """
    title = "Search For Program - With Results Shown"
    programs = Program.objects.all()
    return render(request, 'main/search_program.html', locals())

# @apply_perms
# def result_search_program(request,**kwargs):
#     """
#     display results from a program search.
#     :param request: http get request object
#     :return: renders program search results
#     """
#     query = Q()
#     query_show = ''
#     title = "Search Program- With Results Shown"
#
#
#     if 'a' in request.GET:
#         a = request.GET['a']
#         if a:
#             query = query & (Q(the_name__icontains=a))
#             query_show = query_show + "Program Name = " + str(a) + " "
#
#
#     program_list = Program.objects.filter(query).extra( select={'lower_name': 'lower(the_name)'}).order_by('lower_name')
#     count = len(program_list)
#     query_show = query_show
#
#
#     return render(request, 'main/search_program_result.html', locals())

####################################################################### End Program




########################################################################## Start Extramural Vehicle

@login_required
@apply_perms
def create_vehicle(request,**kwargs):
    user = request.user
    profile = user.userprofile
    title = "Create a New Extramural Vehicle"
    vehicles = ExtramuralVehicle.objects.all()
    #vehicle_types = VehicleType.objects.all().order_by('the_name')

    if request.method == "POST":
        form = ExtramuralVehicleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            vehicle = form.save(commit=False)

            vehicle.user = user
            vehicle.created_by = user.username
            vehicle.last_modified_by = user.username
            vehicle.save()

            url = '/projects/vehicle/show/%s/' % str(vehicle.id)
            return HttpResponseRedirect(url)
    else:
        form = ExtramuralVehicleForm()
    return render(request, 'main/create_extramural_vehicle.html', locals())

@login_required
@apply_perms
def edit_vehicle(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile

    title = "Update Extramural Vehicle"

    vehicle = ExtramuralVehicle.objects.get(id=obj_id)
    vehicles = ExtramuralVehicle.objects.all()

    if request.method == "POST":
        form = ExtramuralVehicleForm(data=request.POST, files=request.FILES, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.last_modified_by = user.username
            vehicle.save()

            url = '/projects/vehicle/show/%s/' % str(vehicle.id)
            return HttpResponseRedirect(url)
    else:
        form = ExtramuralVehicleForm(instance=vehicle)

    return render(request, 'main/edit_extramural_vehicle.html', locals())




@login_required
@never_cache
@apply_perms
def show_vehicle(request, obj_id,**kwargs):
    """
    display detailed view of an extramural vehicle
    :param request:
    :param obj_id:
    :return:
    """
    user = request.user

    vehicle = get_object_or_404(ExtramuralVehicle, id=obj_id)
    form = ExtramuralVehicleForm(instance=vehicle, read_only=True)

    project_list = Project.objects.filter(extramural_vehicle=vehicle).extra( select={'lower_name': 'lower(title)'}).order_by('lower_name')

    return render(request, 'show/show_extramural_vehicle.html', locals())

@apply_perms
def search_vehicle(request,**kwargs):
    """
    displays the search page for extramural vehicles
    :param request:
    :return:
    """
    title = "Search For Extramural Vehicle - With Results Shown"
    vehicles = ExtramuralVehicle.objects.all()
    return render(request, 'main/search_extramural_vehicle.html', locals())

# @apply_perms
# def result_search_vehicle(request,**kwargs):
#     """
#     display results from a program search.
#     :param request: http get request object
#     :return: renders program search results
#     """
#     query = Q()
#     query_show = ''
#     title = "Search Extramural Vehicle- With Results Shown"
#
#
#     if 'a' in request.GET:
#         a = request.GET['a']
#         if a:
#             query = query & (Q(the_name__icontains=a))
#             query_show = query_show + "Program Name = " + str(a) + " "
#
#
#     program_list = ExtramuralVehicle.objects.filter(query).extra( select={'lower_name': 'lower(the_name)'}).order_by('lower_name')
#     count = len(program_list)
#     query_show = query_show
#
#
#     return render(request, 'main/search_program_result.html', locals())

####################################################################### End Extramural Vehicle









########################################################################## Start NRMRLQAPPRequirement

@login_required
@apply_perms
def create_nrmrl(request,**kwargs):
    user = request.user
    profile = user.userprofile
    title = "Create a New NRMRLQAPPRequirement"
    nrmrls = NRMRLQAPPRequirement.objects.all()

    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create NRMRL QAPP Requirements"
#    else:
#        error_message = "You are not authorized to create NRMRL QAPP Requirements."
#        back_link = "/projects/nrmrl/list/"
#        return render(request, 'error.html', locals())


    if request.method == "POST":
        form = NRMRLQAPPRequirementForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            nrmrl = form.save(commit=False)

            nrmrl.user = user
            nrmrl.created_by = user.username
            nrmrl.last_modified_by = user.username
            nrmrl.save()

            url = '/projects/nrmrl/show/%s/' % str(nrmrl.id)
            return HttpResponseRedirect(url)
    else:
        form = NRMRLQAPPRequirementForm()
    return render(request, 'create.html', locals())

@login_required
@apply_perms
def edit_nrmrl(request, obj_id,**kwargs):
    user = request.user

    title = "Update NRMRLQAPPRequirement"

    profile = user.userprofile

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can edit NRMRL QAPP Requirements"
#    else:
#        error_message = "You are not authorized to edit NRMRL QAPP Requirements."
#        back_link = "/projects/nrmrl/list/"
#        return render(request, 'error.html', locals())


    nrmrl = NRMRLQAPPRequirement.objects.get(id=obj_id)
    nrmrls = NRMRLQAPPRequirement.objects.all()

#    if profile.user_type == "SUPER" or user == nrmrl.user:
#        pass
#    else:
#        return render(request, 'no_edit.html', locals())

    if nrmrl.user == user:
        if request.method == "POST":
            form = NRMRLQAPPRequirementForm(data=request.POST, files=request.FILES, instance=nrmrl)
            if form.is_valid():
                nrmrl = form.save(commit=False)

                nrmrl.last_modified_by = user.username
                nrmrl.save()

                url = '/projects/nrmrl/show/%s/' % str(nrmrl.id)
                return HttpResponseRedirect(url)
        else:
            form = NRMRLQAPPRequirementForm(instance=nrmrl)
    else:
        url = '/accounts/not_authorized/'

    return render(request, 'edit.html', locals())

@login_required
@apply_perms
def delete_nrmrl(request, obj_id,**kwargs):
    title = "Delete NRMRLQAPPRequirement"
    user = request.user
    nrmrl = get_object_or_404(NRMRLQAPPRequirement, id=obj_id)

    if nrmrl.user == user:
        nrmrl.delete()

    url = '/projects/type/list/'
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def list_nrmrls(request,**kwargs):
    user = request.user
    title = "NRMRLQAPPRequirement List"
    nrmrls = NRMRLQAPPRequirement.objects.all().order_by('the_name')
    project_statuses = ProjectStatus.objects.all().order_by('the_name')
    return render(request, 'list/list_nrmrls.html', locals())

@login_required
@never_cache
@apply_perms
def show_nrmrl(request, obj_id,**kwargs):
    user = request.user

    obj = get_object_or_404(NRMRLQAPPRequirement, id=obj_id)
    objects = NRMRLQAPPRequirement.objects.all()
    title = "NRMRLQAPPRequirement"

    return render(request, 'show/show.html', locals())

@apply_perms
def search_nrmrl(request,**kwargs):
    title = "Search For NRMRLQAPPRequirement - With Results Shown"
    return render(request, 'main/search_nrmrl.html', locals())

@apply_perms
def result_search_nrmrl(request,**kwargs):
    query = Q()
    query_show = ''
    x = int(0)
    y = int(0)
    title = "Search NRMRLQAPPRequirement- With Results Shown"

    if request is None:
        return NRMRLQAPPRequirement.objects.get(id=1)

    if 'a' in request.GET:
        a = request.GET['a']
        if a:
            query = query & (Q(name__startswith=a))
            query_show = query_show + "User Compound Library Name = " + str(a) + " "

    if 'b' in request.GET:
        b = request.GET['b']
        if b:
            query = query & (Q(cas_number__startswith=b))
            query_show = query_show + "CAS Number = " + str(b) + " "

    if 'c' in request.GET:
        c = request.GET['c']
        if c:
            query = query & (Q(formula__startswith=c))
            query_show = query_show + "Molecular Formula = " + str(c) + " "

    count_per_page = 50

    if 'w' in request.GET:
        w = request.GET['w']
        if 'next' in request.GET:
            next = request.GET['next']
            page = int(page) + 1
            pg = int(page)
        if 'previous' in request.GET:
            previous = request.GET['previous']
            page = int(page) - 1
            if page == 0:
                page = 1
            pg = int(page)
        if 'start' in request.GET:
            start = request.GET['start']
            pg = int(page)

        if pg > 1:
            y = pg * count_per_page

            if y < count_per_page:
                x = 0
            else:
                x = y - count_per_page
        else:
            pg = 1
            y = count_per_page
            x = 0
    else:
        pg = 1
        y = count_per_page
        x = 0

    query = query & (Q(make_public="Y"))

    if query:
        the_count = NRMRLQAPPRequirement.objects.filter(query).count()
        max_page_number = int(floor(the_count/50)) + 1
        if max_page_number <= pg:
            if the_count > count_per_page - 1:
                y = int(the_count)
                x = int(y - count_per_page)
            else:
                y = int(the_count)
                x = 0

        objs = NRMRLQAPPRequirement.objects.filter(query)[x:y]
    else:
        objs = ""

    return render(request, 'main/search_nrmrl.html', locals())

####################################################################### End NRMRLQAPPRequirement


########################################################################## Start EPA Non-ORD Organization
# Originally called "Participating Organization.

@login_required
@apply_perms
def create_participating_organization(request,**kwargs):
    user = request.user
    profile = user.userprofile
    participating_organizations = ParticipatingOrganization.objects.all()

    title = "Create a New EPA Non-ORD Organization"

    if request.method == "POST":
        form = ParticipatingOrganizationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if 'files' in request.FILES:
                files = request.FILES['files']
                files.user = user

            participating_organization = form.save(commit=False)

            participating_organization.user = user
            participating_organization.created_by = user.username
            participating_organization.last_modified_by = user.username
            participating_organization.save()

            url = '/projects/participating_organization/show/%s/' % str(participating_organization.id)
            return HttpResponseRedirect(url)
    else:
        form = ParticipatingOrganizationForm()
    return render(request, 'main/create_participating_organization.html', locals())

@login_required
@apply_perms
def edit_participating_organization(request, obj_id,**kwargs):
    user = request.user

    title = "Update EPA Non-ORD Organization"

    participating_organization = ParticipatingOrganization.objects.get(id=obj_id)
    participating_organizations = ParticipatingOrganization.objects.all()

    if request.method == "POST":
        form = ParticipatingOrganizationForm(data=request.POST, files=request.FILES, instance=participating_organization)
        if form.is_valid():
            participating_organization = form.save(commit=False)

            participating_organization.last_modified_by = user.username
            participating_organization.save()

            url = '/projects/participating_organization/show/%s/' % str(participating_organization.id)
            return HttpResponseRedirect(url)
    else:
        form = ParticipatingOrganizationForm(instance=participating_organization)

    return render(request, 'main/edit_participating_organization.html', locals())

@login_required
@apply_perms
def delete_participating_organization(request, obj_id,**kwargs):
    title = "Delete EPA Non-ORD Organization"
    user = request.user
    participating_organization = get_object_or_404(ParticipatingOrganization, id=obj_id)

#    if participating_organization.user == user or profile.user_type == "SUPER":
    participating_organization.delete()

    url = '/projects/status/list/'
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def list_participating_organizations(request,**kwargs):
    user = request.user
    title = "EPA Non-ORD Organization List"
    participating_organizations = ParticipatingOrganization.objects.all().order_by('the_name')
    return render(request, 'list/list_participating_organizations.html', locals())

@login_required
@never_cache
@apply_perms
def show_participating_organization(request, obj_id,**kwargs):
    user = request.user

    organization = get_object_or_404(ParticipatingOrganization, id=obj_id)

    project_list = Project.objects.filter(participating_organizations=organization).extra(select={'lower_name': 'lower(title)'}).order_by('lower_name')
    form = ParticipatingOrganizationForm(instance=organization, read_only=True)

    return render(request, 'show/show_participating_organization.html', locals())

@login_required
@apply_perms
def search_participating_organization(request,**kwargs):
    title = "Search For EPA Non-ORD Organization - With Results Shown"
    participating_organizations = ParticipatingOrganization.objects.all()
    return render(request, 'main/search_participating_organization.html', locals())

# @login_required
# @apply_perms
# def result_search_participating_organization(request,**kwargs):
#     query = Q()
#     query_show = ''
#     x = int(0)
#     y = int(0)
#     title = "Search EPA Non-ORD Organization - With Results Shown"
#
#     if request is None:
#         return ParticipatingOrganization.objects.get(id=1)
#
#     if 'a' in request.GET:
#         a = request.GET['a']
#         if a:
#             query = query & (Q(company__icontains=a))
#             query_show = query_show + "Program Name = " + str(a) + " "
#
#
#     participating_organization_list = ParticipatingOrganization.objects.filter(query)#.extra( select={'lower_name': 'lower(company)'}).order_by('lower_name')
#     count = len(participating_organization_list)
#     for item in participating_organization_list:
#         print(item.project_set.count())
#     query_show = query_show
#
#     return render(request, 'main/search_participating_organization_result.html', locals())

####################################################################### End EPA Non-ORD Organization
####################################################################### End EPA Non-ORD Organization
####################################################################### End EPA Non-ORD Organization
####################################################################### End EPA Non-ORD Organization




##################################################################################################################################### Start QA Review
##################################################################################################################################### Start QA Review
##################################################################################################################################### Start QA Review
##################################################################################################################################### Start QA Review

@login_required
@never_cache
@apply_perms
def show_review(request, project_log_id,**kwargs):
    project_log = ProjectLog.objects.get(id=project_log_id)
    qa_review_distributions = QaReviewDistribution.objects.filter(project_log=project_log)
    project_attachments = ProjectAttachment.objects.filter(project_log=project_log)

    # Determine latest QAPP QA activity that is approved, if any.
    latestapprovedqapp = ""
    qapp_SQL = (
            "select * from projects_projectlog where project_id = " + str(
        project_log.project_id) + " and project_log_type_id = 3 and date_approved is not NULL ORDER BY date_approved DESC LIMIT 1"
    )
    for latestapprovedqapp in ProjectLog.objects.raw(qapp_SQL):
        latestapprovedqapp = latestapprovedqapp.qa_log_number

    return render(request, 'show/show_qa_review.html', locals())


@login_required
@apply_perms
def edit_review(request, project_log_id,**kwargs):
    user = request.user
    profile = user.userprofile

    title = "Edit: QA Review"
    project_log = ProjectLog.objects.get(id=project_log_id)
    obj = project_log
    project = project_log.project
    qa_review_distributions = QaReviewDistribution.objects.filter(project_log=project_log)
    projectlog_update_history = ProjectLog_update_history.objects.filter(project_log=project_log)

    # Determine if a review is being created or edited.
    if obj.review_type is not None or obj.qa_review_comment is not None:
        creating = False
    else:
        creating = True

#    if profile.user_type == "SUPER" or profile.can_edit == "Y":
    error_message = "You can create QA Reviews"
#    else:
#        error_message = "You are not authorized to create QA Reviews."
#        back_link = "/projects/qlog/show/%s/" % str(project_log.id)
#        return render(request, 'error.html', locals())


#    if profile.is_reviewer == "Y":

    # Determine latest QAPP QA activity that is approved, if any.
    latestapprovedqapp = ""
    qapp_SQL = (
            "select * from projects_projectlog where project_id = " + str(
        obj.project_id) + " and project_log_type_id = 3 and date_approved is not NULL ORDER BY date_approved DESC LIMIT 1"
    )
    for latestapprovedqapp in ProjectLog.objects.raw(qapp_SQL):
        latestapprovedqapp = latestapprovedqapp.qa_log_number


    if request.method == "POST":
        form = QaReviewFormAsync(data=request.POST, instance=project_log)

        before_review_type = obj.review_type
        before_reviewer = obj.reviewer
        before_qa_review_comment = obj.qa_review_comment
        before_qapp_status = project.qapp_status
        before_qapp_approval_date = project.qapp_approval_date
        before_last_qapp_review_date = project.last_qapp_review_date
        update_comments = request.POST.get("update_comment")

        if form.is_valid():

            instance = form.save(commit=False)

            instance.date_reviewed = timezone.now()
            if instance.date_approved == '' or instance.date_approved is None:
                instance.date_approved = None
            if instance.date_received == '' or instance.date_received is None:
                instance.date_received = None
            if instance.review_type is not None:
                if (instance.review_type.the_name == "Approved" or instance.review_type.the_name == "Approved with minor revisions") and instance.date_approved is None:
                    instance.date_approved = timezone.now()

            # Check if project fields should be updated as a result of a QAPP QA activity update.
            if instance.project_log_type.the_name == 'QAPP':

                if instance.date_received is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Review')
                else:
                    pass

                if instance.date_reviewed is not None:
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP in Revision')
                else:
                    pass

                if instance.date_approved is not None:
                    project.qapp_approval_date = instance.date_approved
                    project.qapp_status = QappStatus.objects.get(the_name='QAPP Approved')
                    if project.last_qapp_review_date is not None:
                        if instance.date_approved.date() > project.last_qapp_review_date:
                            project.last_qapp_review_date = instance.date_approved
                    else:
                        project.last_qapp_review_date = instance.date_approved
                else:
                    pass
                # project.save()

                # Add entry to project update history if project's fields changed (Only for QAPP QA activities).
                log_hist = False

                if before_qapp_status != project.qapp_status:
                    log_hist = True
                elif before_qapp_approval_date != project.qapp_approval_date:
                    log_hist = True
                elif before_last_qapp_review_date != project.last_qapp_review_date:
                    log_hist = True

                if log_hist:
                    # If user hasn't entered update comment, then add default.
                    if not update_comments:
                        if creating == True:
                            update_comments = 'QAPP QA activity review created'
                        else:
                            update_comments = 'QAPP QA activity review edited'

                    # add to project update history
                    project_update_history = Project_update_history.objects.create(project=project,
                                                                                   user=user,
                                                                                   date_qappreviewed=project.last_qapp_review_date,
                                                                                   projectlead=project.person,
                                                                                   qa_manager=project.qa_manager,
                                                                                   project_status=project.project_status,
                                                                                   qapp_status=project.qapp_status,
                                                                                   comments=update_comments)

            else:
                pass

            instance.last_modified_by = user.username

            # Need to save these before we create the PDF, otherwise the PDF emailed
            # doesn't have the latest data.
            project.save()
            instance.save()
            pdf_file = pdf_qlog(request, instance.id, make_pdf_file=1)

            instance.attachment_pdf = "%s/qa_reviews/qa_review_%s.pdf" % (str(user.username), str(instance.qa_log_number))
            instance.save()
            form.save_m2m()


            # Add entry to QA activity update history if review created or if key fields changed when editing.
            if creating == True:
                log_hist = True
                # If user hasn't entered update comment, then add default.
                if not update_comments:
                    update_comments = 'QA activity review created'
            else:
                log_hist = False

                if before_review_type != instance.review_type:
                    log_hist = True
                elif before_reviewer != instance.reviewer:
                    log_hist = True
                elif before_qa_review_comment != instance.qa_review_comment:
                    log_hist = True
                    if not update_comments:
                        update_comments = 'QA activity review comments edited'
                elif update_comments:
                    log_hist = True

                # If user hasn't entered update comment, then add default.
                if not update_comments:
                    update_comments = 'QA activity review edited'

            if log_hist:
                # add entry to QA activity update history
                projectlog_update_history = ProjectLog_update_history.objects.create(project_log=project_log,
                                                                                     user=user,
                                                                                     date_approved=instance.date_approved,
                                                                                     review_type=instance.review_type,
                                                                                     technical_lead=instance.technical_lead,
                                                                                     reviewer=instance.reviewer,
                                                                                     comments=update_comments)

            project_log_qa_review_attachments = ProjectAttachment.objects.filter(Q(project_log=project_log) & Q(where_from="QA Review"))

            if 'send_the_emails' in request.POST:
                the_pdf = settings.MEDIA_ROOT + str(instance.attachment_pdf)
                email_list = []
                with open(the_pdf, 'rb') as f:
                    the_content = f.read()

                # Moved this lower in order to create a string with ORD and non-ORD emails first.
                #the_time = timezone.now() - timedelta(seconds=14400)
                #qa_review_distribution = QaReviewDistribution.objects.create(project_log=instance,
                #                                                             the_name="Date: " + the_time.strftime(
                #                                                                 "%Y-%m-%d %I:%M %p EST") + " Emails sent to " + instance.qa_review_email_list)

                ### Make sure to strip out semicolons
                email_list = [user.email]
                for w in instance.qa_review_email_list.split():
                    w = w.replace(';','')
                    w = w.replace(',','')
                    email_list.append(w)

                # Create a string with all the ORD and non-ORD emails.
                # This is used to create the string that logs who emails were sent to for distribution.
                # Added the user.email as well since it looks strange to have no emails listed
                # # if no one is in the distribution list. An email is still sent to the user.
                all_emails = user.email + ' ' + instance.qa_review_email_list

                for d in instance.qa_review_distribution_list.all():
                    email_list.append(d.email)
                    all_emails = all_emails + ' ' + d.email

                # Include the project QA Manager since that field has been added to projects
                if project.qa_manager != None:
                    email_list.append(project.qa_manager.email)
                # Include the reviewer.
                if instance.reviewer != None:
                    email_list.append(instance.reviewer.email)
                # Remove any duplicates since reviewer is often the same as project QA manager and may also be the user.
                email_list = list(set(email_list))

                from_email = settings.DEFAULT_FROM_EMAIL

                # Only include RAP number in subject if there is one.
                rap_fields = get_rap_fields('projects')
                rapVals = []
                for rap in rap_fields:
                    valString = getattr(project,rap)
                    if valString != '' and valString is not None:
                        valString = str(valString)
                        spl = rap.split('_')
                        title = spl[0].upper()
                        valueList = sort_rap_numbers(re.split(r'; |, |;|,',valString))
                        valueList = [title + ' ' + val for val in valueList]
                        rapVals = rapVals + valueList

                rap_info = ''
                if len(rapVals):
                    rap_info = "RAP Project(s) " + ', '.join(rapVals) + ': '

                email_subject = rap_info + 'QA Track Review for QA Activity ' + instance.qa_log_number

                # Compose the email message.
                email_body = 'Attached are the QA Review form and associated comments (if applicable) for:' + '\n\nQA Activity:  ' + instance.qa_log_number + '\r\n'

                # Include alternate and previous IDs, if any.
                if instance.alt_id:
                    email_body = email_body + "Alternate ID:  " + instance.alt_id + "\r\n"
                if instance.previous_id:
                    email_body = email_body + "Previous ID:  " + instance.previous_id + "\r\n"

                email_body = email_body + 'Title:  ' + instance.title + '\r\nType:  ' + instance.project_log_type.the_name + '\r\nPOC:  ' + instance.technical_lead.first_name + ' ' + instance.technical_lead.last_name


                # Send one email, include everyone.
                the_email = createQTEmailMessage(email_subject, email_body, from_email, email_list, [])

                the_email.attach_file(the_pdf, 'application/pdf')

                for af in project_log_qa_review_attachments:
                    the_file = settings.MEDIA_ROOT + str(af.attachment)
                    the_email.attach_file(the_file)

                the_email.send(fail_silently=False)

                # Logging the email send now so it doesn't get logged if there was an error on the send.
                # the_time = timezone.now() - timedelta(seconds=14400)
                the_time = timezone.now()
                qa_review_distribution = QaReviewDistribution.objects.create(project_log=instance,
                                                                             the_name="Date: " + the_time.strftime(
                                                                                 "%Y-%m-%d %I:%M %p EST") + " Emails sent to " + all_emails)

                url = '/projects/qa_review/show/%s/' % str(instance.id)
                return HttpResponseRedirect(url)

            if 'just_update' in request.POST:
                url = '/projects/qa_review/show/%s/' % str(instance.id)
                return HttpResponseRedirect(url)

            url = '/projects/qa_review/edit/%s/' % str(instance.id)
            return HttpResponseRedirect(url)
    else:
        form = QaReviewFormAsync(instance=project_log)

#    else:
#        error = "You are not authorized to edit a QA Activity Review"
#        return render(request, 'show/show_qa_review.html', locals())

    return render(request, 'main/edit_review.html', locals())

@login_required
@apply_perms
def qa_review_pending(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division
    #selected_branch = user.userprofile.branch

    # formatting for the organization selector
    label_class = "col-sm-3"
    input_container_class = "col-sm-9"

    title = "Search Pending QA Reviews"

    if "search" in request.GET:
        subheader = "Pending QA Reviews"
        query = Q()
        query_show = ''

        office_id = request.GET.get("office", None)
        lab_id = request.GET.get("lab", None)
        division_id = request.GET.get("division", None)
        branch_id = request.GET.get("branch", None)

        if office_id is not None and office_id != '':
            office = Office.objects.get(id = office_id)
            query = query & (Q(division__office__id=office_id))
            query_show = query_show + "Office = " + str(office.abbreviation) + ", "

        if lab_id is not None and lab_id != '':
            lab = Lab.objects.get(id = lab_id)
            query = query & (Q(division__lab__id=lab_id))
            query_show = query_show + "Center = " + str(lab.abbreviation) + ", "

        if division_id is not None and division_id != '':
            division = Division.objects.get(id = division_id)
            query = query & (Q(division__id=division_id))
            query_show = query_show + "Division = " + str(division.abbreviation) + ", "

        if branch_id is not None and branch_id != '':
            branch = Branch.objects.get(id = branch_id)
            query = query & (Q(branch__id=branch_id))
            query_show = query_show + "Branch = " + str(branch.abbreviation) + ", "

        if 'e' in request.GET:
            e = request.GET['e']
            if e:
                query = query & (Q(reviewer__last_name__istartswith=e))
                query_show = query_show + "Reviewer Last Name starts with " + str(e) + ", "

        if 'f' in request.GET:
            f = request.GET['f']
            if f:
                query = query & (Q(reviewer__first_name__istartswith=f))
                query_show = query_show + "Reviewer First Name starts with " + str(f) + ", "

        query = (query  & Q(qa_review_required="Y") & Q(date_reviewed__isnull=True) & Q(date_approved__isnull=True))

        # Clean up dangling comma.
        last_two = query_show[len(query_show) - 2:]
        if last_two == ', ':
            query_show = query_show[:-2]

        objs = ProjectLog.objects.filter(query)
        the_count = len(objs)

    return render(request, 'list/list_pending_qa_reviews.html', locals())

@login_required
@apply_perms
def search_qa_review(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division

    # formatting for the organization selector
    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    query = Q()
    query_show = ''
    the_count = 0
    title = "Search For QA Activities - With Results Shown"
    project_log_types = ProjectLogType.objects.all().order_by('the_name')
    product_category_types = ProductCategory.objects.all().order_by('sort_number')
    review_types = ReviewType.objects.all().order_by('the_name')

    return render(request, 'main/search_qa_review.html', locals())

@login_required
@apply_perms
def result_search_qa_review(request,**kwargs):
    user = request.user

    query = Q()
    query_show = ''
    the_count = 0
    title = "Search For QA Activities - With Results Shown"
    project_log_types = ProjectLogType.objects.all().order_by('the_name')

    if request is None:
        return ProjectLog.objects.get(id=1)

    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id = office_id)
        query = query & (Q(office__id=office_id))
        query_show = query_show + "Office = " + str(office.abbreviation) + ", "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id = lab_id)
        query = query & (Q(lab__id=lab_id))
        query_show = query_show + "Center = " + str(lab.abbreviation) + ", "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id = division_id)
        query = query & (Q(division__id=division_id))
        query_show = query_show + "Division = " + str(division.abbreviation) + ", "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id = branch_id)
        query = query & (Q(branch__id=branch_id))
        query_show = query_show + "Branch = " + str(branch.abbreviation) + ", "

    if 'kw' in request.GET:
        kw = request.GET['kw']
        if kw:
            query = query & (Q(program__the_name__icontains=kw))
            query_show = query_show + "Keyword = " + str(kw) + ", "

    if 'qa_activity_id' in request.GET:
        qa_activity_id = request.GET['qa_activity_id']
        qa_activity_id = qa_activity_id.strip()  # Trim white space
        if qa_activity_id:
            query = query & (Q(qa_log_number__icontains=qa_activity_id))
            query_show = query_show + "QA Activity ID contains " + str(qa_activity_id) + ", "

    if 'alt_id' in request.GET:
        alt_id = request.GET['alt_id']
        alt_id = alt_id.strip()  # Trim white space
        if alt_id:
            query = query & (Q(alt_id__icontains=alt_id))
            query_show = query_show + "Alternate ID contains " + str(alt_id) + ", "

    if 'previous_id' in request.GET:
        previous_id = request.GET['previous_id']
        previous_id = previous_id.strip()  # Trim white space
        if previous_id:
            query = query & (Q(previous_id__icontains=previous_id))
            query_show = query_show + "Previous ID contains " + str(previous_id) + ", "

    if 'c' in request.GET:
        c = request.GET['c']
        if c:
            query = query & (Q(technical_lead__last_name__istartswith=c))
            query_show = query_show + "QA Activity POC Last Name starts with " + str(c) + ", "

    if 'fn' in request.GET:
        fn = request.GET['fn']
        if fn:
            query = query & (Q(technical_lead__first_name__istartswith=fn))
            query_show = query_show + "QA Activity POC First Name starts with " + str(fn) + ", "

    if 't' in request.GET:
        t = request.GET['t']
        if t:
            query = query & (Q(project__person__last_name__istartswith=t))
            query_show = query_show + "Project Lead Last Name = starts with " + str(t) + ", "

    if 'v' in request.GET:
        v = request.GET['v']
        if v:
            query = query & (Q(project__person__first_name__istartswith=v))
            query_show = query_show + "Project Lead First Name starts with " + str(v) + ", "

    if 'e' in request.GET:
        e = request.GET['e']
        if e:
            query = query & (Q(reviewer__last_name__istartswith=e))
            query_show = query_show + "Reviewer Last Name starts with " + str(e) + ", "

    if 'f' in request.GET:
        f = request.GET['f']
        if f:
            query = query & (Q(reviewer__first_name__istartswith=f))
            query_show = query_show + "Reviewer First Name starts with " + str(f) + ", "

    item_01 = ''
    sub_query_01 = Q()
    sub_query_show_01 = ''
    if 'r' in request.GET:
        r = request.GET.getlist('r')
        if r:
            for item_01 in r:
                sub_query_01 = sub_query_01 | Q(project_log_type__the_name__iexact=item_01)
                sub_query_show_01 = sub_query_show_01 + str(item_01) + ", "

            query = sub_query_01 & query
            query_show = query_show + "QA Activity Type(s) => " + sub_query_show_01

    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'product_categories' in request.GET:
        product_categories = request.GET.getlist('product_categories')
        if product_categories:
            for item_03 in product_categories:
                sub_query_03 = sub_query_03 | Q(product_category__the_name__iexact=item_03)
                sub_query_show_03 = sub_query_show_03 + str(item_03) + ", "

            query = sub_query_03 & query
            query_show = query_show + "Product Category(ies) => " + sub_query_show_03

    item_02 = ''
    sub_query_02 = Q()
    sub_query_show_02 = ''
    if 'rt' in request.GET:
        rt = request.GET.getlist('rt')
        if rt:
            for item_02 in rt:
                sub_query_02 = sub_query_02 | Q(project_log_type__the_name__iexact=item_02)
                sub_query_show_02 = sub_query_show_02 + str(item_02) + ", "

            query = sub_query_02 & query
            query_show = query_show + "Review Recommendation(s) => " + sub_query_show_02

    if 'g' in request.GET:
        g = request.GET['g']
        if g:
            query = query & (Q(date_received__gte=g))
            query_show = query_show + "QA Activity Received From Date = " + str(g) + ", "

    if 'dh' in request.GET:
        dh = request.GET['dh']
        if dh:
            query = query & (Q(date_received__lte=dh))
            query_show = query_show + "QA Activity Received To Date = " + str(dh) + ", "

    if 'j' in request.GET:
        j = request.GET['j']
        if j:
            query = query & (Q(date_reviewed__gte=j))
            query_show = query_show + "QA Activity Reviewed From Date = " + str(j) + ", "

    if 'k' in request.GET:
        k = request.GET['k']
        if k:
            query = query & (Q(date_reviewed__lte=k))
            query_show = query_show + "QA Activity Received To Date = " + str(k) + ", "

    if 'm' in request.GET:
        m = request.GET['m']
        if m:
            query = query & (Q(date_approved__gte=m))
            query_show = query_show + "QA Activity Approved From Date = " + str(m) + ", "

    if 'n' in request.GET:
        n = request.GET['n']
        if n:
            query = query & (Q(date_approved__lte=n))
            query_show = query_show + "QA Activity Approved To Date = " + str(n) + ", "


    if 'tl' in request.GET:
        tl = request.GET['tl']
        if tl:
            query = query & (Q(title__icontains=tl))
            query_show = query_show + "Title contains " + str(tl) + ", "

    if 'project_qa_id' in request.GET:
        project_qa_id = request.GET['project_qa_id']
        project_qa_id = project_qa_id.strip()  # Trim white space
        if project_qa_id:
            query = query & (Q(project__qa_id__icontains=project_qa_id))
            query_show = query_show + "Project QA ID contains " + str(project_qa_id) + ", "


    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    objs = ProjectLog.objects.filter(query).all()
    the_count = len(objs)
    query_show = query_show


    rap_fields = get_rap_fields()

    for obj in objs:
        obj.rap = []
        project = obj.project
        for rap in rap_fields:
            valString = getattr(project,rap)
            if valString != '' and valString is not None:
                valString = str(valString)
                if rap == 'hsrp_rap_extensions':
                    program = 'HSRP Extensions'
                else:
                    program = rap.split('_')[0].upper()
                valueList = sort_rap_numbers(re.split(r'; |, |;|,',valString))
                values = ', '.join(valueList)
                if not values.startswith(program):
                    values = program + ' ' + values
                row = {'values':values}
                obj.rap.append(row)


    return render(request, 'main/search_qa_review_result.html', locals())



@login_required
@csrf_exempt
@apply_perms
def ajax_lookup_divisions(request, lab,**kwargs):
    current_lab = Lab.objects.get(abbreviation=lab)
    divisions = Division.objects.all().filter(lab=current_lab)
    json_models = serializers.serialize("json", divisions)
    return HttpResponse(json_models, content_type='application/javascript')

@login_required
@csrf_exempt
@apply_perms
def ajax_lookup_branches(request, division,**kwargs):
    current_division = Division.objects.get(abbreviation=division)
    branches = Branch.objects.all().filter(division=current_division)
    json_models = serializers.serialize("json", branches)
    return HttpResponse(json_models, content_type='application/javascript')

@login_required
@apply_perms
def switch_qapp_review_file_flag(request, obj_id ,**kwargs):
    # return HttpResponse('<p>OBJ ID {0}</p>'.format(obj_id))
    user = request.user
    project_attachment = get_object_or_404(ProjectAttachment, id=obj_id)

    # Do not allow toggling if the file is marked as the latest approved QAPP file.
    if project_attachment.is_latest_qapp_doc == "N" and project_attachment.is_latest_qapp_pdf == "N":
        if project_attachment.is_qapp_review_file != "Y":
            project_attachment.is_qapp_review_file = "Y"
        else:
            project_attachment.is_qapp_review_file = "N"

    project_attachment.save()
    print(project_attachment.project_log_id)

#    if fromtable=='activity':

    if project_attachment.project_log_id is not None:
        url = '/projects/show_expanded/%s/#activity_attachments' % str(project_attachment.project_id)
    else:
        url = '/projects/show_expanded/%s/#attachments' % str(project_attachment.project_id)

    return HttpResponseRedirect(url)

@login_required
@apply_perms
def switch_latest_qapp_flag(request, obj_id, **kwargs):
    attachment = get_object_or_404(ProjectAttachment, id=obj_id)
    referer_url = request.META['HTTP_REFERER']

#    if fromtable=='activity':
    if attachment.project_log_id is not None:
        redirect_url = '/projects/show_expanded/%s/#activity_attachments' % str(attachment.project_id)
        #redirect_url = referer_url + '#activity_attachments'
    else:
        redirect_url = '/projects/show_expanded/%s/#attachments' % str(attachment.project_id)
        #redirect_url = referer_url + '#attachments'


    attachment_type = get_file_type(attachment.the_name)

    if attachment_type == 'doc':
        # if it is latest 'Y' set to 'N' and redirect
        if attachment.is_latest_qapp_doc == 'Y':
            attachment.is_latest_qapp_doc = 'N'
            attachment.is_qapp_review_file = 'N' # Don't include in reminder anymore.
            attachment.save()

        # else we're making it the latest, so unset others
        else:
            qapp_attachments = ProjectAttachment.objects.filter(project=attachment.project)
            for att in qapp_attachments:
                if get_file_type(att.the_name) == 'doc':
                    if att.is_latest_qapp_doc == 'Y':
                        att.is_qapp_review_file = 'N'
                    att.is_latest_qapp_doc = 'N'
                    att.save()

            attachment.is_latest_qapp_doc = 'Y'
            attachment.is_qapp_review_file = 'Y'
            attachment.save()

    elif attachment_type == 'pdf':
        # if it is latest 'Y' set to 'N' and redirect
        if attachment.is_latest_qapp_pdf == 'Y':
            attachment.is_latest_qapp_pdf = 'N'
            attachment.is_qapp_review_file = 'N'  # Don't include in reminder anymore.
            attachment.save()

        # else we're making it the latest, so unset others
        else:
            qapp_attachments = ProjectAttachment.objects.filter(project=attachment.project)
            for att in qapp_attachments:
                if get_file_type(att.the_name) == 'pdf':
                    if att.is_latest_qapp_pdf == 'Y':
                        print(att.the_name)
                        att.is_qapp_review_file = 'N'
                    att.is_latest_qapp_pdf = 'N'
                    att.save()

            attachment.is_latest_qapp_pdf = 'Y'
            attachment.is_qapp_review_file = 'Y'
            attachment.save()

    return HttpResponseRedirect(redirect_url)


class CreateOrgLink_Project(FormView):
    template = "main/link_organization_proj.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id,**kwargs):

        user = request.user

        # get the organization data
        office_list = oq.get_unrestricted_office_list(user, as_json=True)
        lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
        division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
        branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

        office_required = True
        lab_required = False
        division_required = False
        label_class = "col-sm-3"
        input_container_class = "col-sm-9"

        selected_office = user.userprofile.office

        return render(request, self.template, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, obj_id,**kwargs):
        """
        Create the Org Link (entry into linking table)
        """

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        if (office_id):

            org_link = Project_Orgs()
            project = get_object_or_404(Project, id=obj_id)
            org_link.project = project

            office = get_object_or_404(Office, id=office_id)
            org_link.office = office

            if(lab_id):
                lab = get_object_or_404(Lab, id=lab_id)
                org_link.lab = lab

                if (division_id):
                    division = get_object_or_404(Division, id=division_id)
                    org_link.division = division

                    if (branch_id):
                        branch = get_object_or_404(Branch, id=branch_id)
                        org_link.branch = branch

            org_link.save()

            url = '/projects/show/%s/#relatedorgs' % str(obj_id)
            return HttpResponseRedirect(url)

        else:
            error = "Please select at least an office"

            user = request.user

            # get the organization data
            office_list = oq.get_unrestricted_office_list(user, as_json=True)
            lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
            division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
            branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

            office_required = True
            lab_required = False
            division_required = False
            label_class = "col-sm-3"
            input_container_class = "col-sm-9"

            selected_office = user.userprofile.office

            return render(request, self.template, locals())

@login_required
@apply_perms
def delete_proj_org(request, obj_id,**kwargs):
    user = request.user
    project_org = get_object_or_404(Project_Orgs, id=obj_id)

#    if user.is_staff:
    project_org.delete()

    url = '/projects/show/%s/#relatedorgs' % str(project_org.project_id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def project_test(request,**kwargs):
    return render(request, 'main/project_test.html', locals())

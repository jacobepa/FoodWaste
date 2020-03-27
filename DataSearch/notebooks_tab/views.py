from django.shortcuts import render

from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.postgres.aggregates import *

from django.http import Http404, HttpResponseRedirect, HttpResponse

from projects.models import *

from notebooks_tab.models import *

from .forms import *
from django.utils.decorators import method_decorator
from django.views.generic import FormView

import organization.query_utils as oq

from organization.models import *

# from django.contrib.auth.models import User, Permission

from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from datetime import datetime, timedelta
from django.utils import timezone
# from time import gmtime, strftime, localtime
import time

import xlwt

from django.http import HttpResponse  # for testing
# return HttpResponse("G")   test only


from django.shortcuts import render, redirect

import os

# Added to handle exporting to Excel
import io
import xlsxwriter

from constants.models import *

# imports for sending email notification
import platform
from django.template.loader import get_template

from constants.perms import apply_perms

@login_required
@apply_perms
def index(request,**kwargs):
    user = request.user
    title = "Notebooks Main Page"

    # The main Notebook page displays info about the reviews.
    # Get the sample email text to display.
    html_file = os.path.join(os.path.dirname(__file__), 'templates/nbReviewRequest.txt')
    f = open(html_file, 'r')

    return render(request, 'main/nb_tab.html', locals())

# Create Notebook record
class NotebooksTabCreateView(FormView):

    form_class = NotebooksTabFormAsync
    template = 'main/create_nb_tab_item.html'

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id,**kwargs):

        form = self.form_class()

        user = request.user

        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)
        label_class = "col-sm-4"
        input_container_class = "col-sm-8"
        no_branches = False
        office_required = True
        lab_required = True
        division_required = True

        # set office default
        selected_office = user.userprofile.office

        # # Display the create form
        # if not((obj_id is None) or (obj_id=='0')):
        #     # Got here from Add Audit to Project menu choice.
        #     # Select the project as initial value of projects field.
        #     # Fill in the Lead Organization fields from the project organization.
        #     query = (Q(id__exact=obj_id))
        #     project_queryset = Project.objects.filter(query)
        #     selected_office = project_queryset[0].office
        #     selected_lab = project_queryset[0].lab
        #     selected_division = project_queryset[0].division
        #
        #     form = self.form_class(initial={'projects': project_queryset})  # set default

        return render(request, self.template, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, obj_id, *args, **kwargs):

        # Save the changes to the form
        user = request.user
        form = self.form_class(data=request.POST, files=request.FILES)

        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)
        label_class = "col-sm-4"
        input_container_class = "col-sm-8"
        no_branches = False
        office_required = True
        lab_required = True
        division_required = True

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        if form.is_valid():
            notebookstab = form.save(commit=False)
            notebookstab.user = user

            notebookstab.save()
            form.save_m2m()

            # make the notebook number
            lab = get_object_or_404(Lab, id=lab_id)
            lab_code = "H" if lab.designation_code is None else str(lab.designation_code)
            division = get_object_or_404(Division, id=division_id)
            nb_prefix = lab_code + "-" + str(division.abbreviation)
            if branch_id:
                branch_obj = get_object_or_404(Branch, id=branch_id)
                nb_prefix += "-" + str(branch_obj.abbreviation)

            notebookstab.nb_number = nb_prefix + "-NB-" + str(notebookstab.id)
            notebookstab.save()

            # add to approval history
            nb_approval_history = NotebooksTab_approval_history.objects.create(nbtab=notebookstab,
                                                                             user=user,
                                                                             custodian=notebookstab.custodian,
                                                                             qa_manager=notebookstab.qa_manager,
                                                                             supervisor_mentor=notebookstab.supervisor_mentor,
                                                                             status=notebookstab.status,
                                                                             comments='Notebook created')

            url = '/notebooks_tab/show/%s/' % str(notebookstab.id)
            return HttpResponseRedirect(url)
        else:

            selected_office = Office.objects.get(id=office_id) if oq._valid_org_id(office_id) else None
            selected_lab = Lab.objects.get(id=lab_id) if oq._valid_org_id(lab_id) else None
            selected_division = Division.objects.get(id=division_id) if oq._valid_org_id(division_id) else None
            selected_branch = Branch.objects.get(id=branch_id) if oq._valid_org_id(branch_id) else None

            return render(request, self.template, locals())

@login_required
@apply_perms
def show_nb_tab(request, obj_id,**kwargs):
    user = request.user
    title = "Show Notebook"
    obj = get_object_or_404(NotebooksTab, id=obj_id)
    nb_attachments = NotebooksTabAttachment.objects.filter(nbtab=obj)
    nb_review_distributions = NotebooksTabReviewDistribution.objects.filter(nbtab=obj)
    nb_approval_history = NotebooksTab_approval_history.objects.filter(nbtab=obj)
    orgs = NotebooksTab_Orgs.objects.filter(nbtab=obj)
    reviews = NotebooksTab_Reviews.objects.filter(nbtab=obj)
    review_ids = [r.id for r in reviews]
    review_attachments = NotebooksTabReviewAttachment.objects.filter(review_id__in=review_ids)
    show_nb_review = True
    nb_id = obj.id

    #custodian/contributor info
    users = NotebooksTab_User_Notebooks.objects.filter(nbtab_ids__contains=[obj_id])
    for nb_user in users:
        nb_ids = list(nb_user.nbtab_ids)
        roles = list(nb_user.roles)
        nb_user.this_nb_review = NotebooksTab_Reviews.objects.filter(user_id=nb_user.user_id,nbtab_id=obj_id).first()
        nb_user.sr = NotebooksTab_Schedule_Review.objects.filter(nbtab_id=obj_id,user=nb_user.user).first()

        nbs = NotebooksTab.objects.filter(pk__in=nb_ids)
        has_active_notebooks = False
        #A user doesn't need review if they have no active notebooks
        for nb in nbs:
            if nb.status_id == 1:
                has_active_notebooks = True

        nb_id = int(obj_id)
        if nb_ids.count(nb_id) > 1:
            role = 'Custodian/Contributor'
        else:
            role = roles[nb_ids.index(int(nb_id))].capitalize()
        nb_user.role = role

        a_year_ago = timezone.now().date() - timedelta(days=365)

        try:
            nb_user.needs_review = 'N' if ( not has_active_notebooks or nb_user.recent_review.date_reviewed > a_year_ago ) else 'Y'
        except AttributeError:
            nb_user.needs_review = 'Y'


    # Split out data from each log string so we can show it nicely in web page.
    parsed_logs = []
    if nb_review_distributions:
        for log in nb_review_distributions:
            logstr = log.the_name
            parsed_logs.append(logstr.split(CORRESPONDENCE_LOG_SPLITTER))

    # Fill email subject line form field with default value.
    if obj.title:
        email_subject = "[Notebook " + str(obj.nb_number) + "] " + obj.title
    else:
        email_subject = "Notebook " + str(obj.nb_number)

    if request.method == "POST":

            from_email = settings.DEFAULT_QATRACK_EMAIL

            #  Correspondence is sent to the user, the Notebook Custodian, Supervisor/Mentor,
            # QA Manager, and anyone in the Email Lists

            # Usually the user is also the contact or QA Manager or supervisor/mentor, so don't add email twice.
#            if user.email==obj.custodian.email or user.email==obj.qa_manager.email or user.email==obj.supervisor_mentor:
#                to_emails = [obj.custodian.email, obj.qa_manager.email, obj.supervisor_mentor.email]
#            else:
#                to_emails = [user.email, obj.custodian.email, obj.qa_manager.email, obj.supervisor_mentor.email]
            to_emails = [user.email]
            if obj.custodian is not None:
                to_emails.append(obj.custodian.email)
            if obj.qa_manager is not None:
                to_emails.append(obj.qa_manager.email)
            if obj.supervisor_mentor is not None:
                to_emails.append(obj.supervisor_mentor.email)

            if obj.nb_review_email_list is not None and len(obj.nb_review_email_list) > 0:
                for nonOrd in obj.nb_review_email_list.split():
                    nonOrd = nonOrd.replace(';', '')
                    nonOrd = nonOrd.replace(',', '')
                    to_emails.append(nonOrd)

            for ord_list in obj.nb_review_distribution_list.all():
                to_emails.append(ord_list.email)

            # to_emails = [user.email]   # testing only

            if request.POST.get('include_contributors'):
                for ord_contrib in obj.ord_contributors.all():
                    to_emails.append(ord_contrib.email)

                if obj.non_ord_contributors is not None and len(obj.non_ord_contributors) > 0:
                    for nonOrd in obj.non_ord_contributors.split():
                        nonOrd = nonOrd.replace(';', '')
                        nonOrd = nonOrd.replace(',', '')
                        to_emails.append(nonOrd)


            to_emails = list(set(to_emails)) #remove duplicate emails

            all_emails = ""
            for each_mail in to_emails:
                all_emails += "; " + each_mail

            email_notes = request.POST.get("email_notes", "")
            # Subject is now editable field.
            email_subject = request.POST.get("email_subject", "")
            title = obj.title if obj.title is not None else "Untitled";
            nb_number = obj.nb_number if obj.nb_number is not None else "";
            email_body = "Notebook Number: " + nb_number + "\r\n"

            # Include alternate and previous IDs, if any.
            if obj.alt_id:
                email_body = email_body + "Alternate ID: " + obj.alt_id + "\r\n"
            if obj.previous_id:
                email_body = email_body + "Previous ID: " + obj.previous_id + "\r\n"

            email_body = email_body + "Notebook Title: " + title + "\r\n\r\n"
            email_body_log = email_body.replace("\r\n\r\n", "; ")
            email_body_log = email_body_log.replace("\r\n", "; ")

            # Add project id and title for any linked projects
            projects = obj.projects.all()
            if projects:
                email_body = email_body + "Projects:\r\n"
                email_body_log += "Projects: "
                for proj in projects:
                    email_body = email_body + proj.qa_id + '   ' + proj.title + "\r\n"
                    email_body_log += proj.qa_id + ' ' + proj.title + ", "
                email_body = email_body + '\r\n'
                email_body_log = email_body_log[:-2] + "; "

            # Add any user message.
            email_body = email_body + email_notes

            if email_notes != "":
                email_body_log += "Message: " + email_notes
            else:
                email_body_log = email_body_log[:-2]

            # Make to emails unique.
            to_emails = list(set(to_emails))

            the_email = createQTEmailMessage(email_subject, email_body, from_email, to_emails)

            att_listing = ""
            for att in review_attachments:
                if att.include_in_email == "Y":
                    the_file = settings.MEDIA_ROOT + "/" + str(att.attachment)
                    the_email.attach_file(the_file)
                    att_listing += ", " + att.the_name

            if att_listing == "":
                att_listing = "None"
            else:
                att_listing = att_listing[2:]

            the_email.send(fail_silently=False)

            # add to correspondence log
            the_time = timezone.now() - timedelta(seconds=14400)
            nb_review_distribution = NotebooksTabReviewDistribution.objects.create(nbtab=obj,
                                                      the_name=the_time.strftime("%Y-%m-%d %I:%M %p EST") +
                                                               CORRESPONDENCE_LOG_SPLITTER + all_emails[2:] +
                                                               CORRESPONDENCE_LOG_SPLITTER + email_subject +
                                                               CORRESPONDENCE_LOG_SPLITTER + att_listing +
                                                               CORRESPONDENCE_LOG_SPLITTER + email_body_log)

            url = '/notebooks_tab/show/%s/#correspondence' % str(obj.id)
            return HttpResponseRedirect(url)

    return render(request, 'show/show_nb_tab_item.html', locals())

@login_required
@apply_perms
def file_upload_nbtab(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile
    nbtab = NotebooksTab.objects.get(id=obj_id)

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/notebooks_tab/show/"
#        return render(request, 'error.html', locals())

    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        nbtab_attachment, created = NotebooksTabAttachment.objects.get_or_create(nbtab=nbtab, attachment=new_file,
                                                                            the_name=new_file.name, user=user,
                                                                            the_size=new_file.size)

    url = '/notebooks_tab/show/%s/#attachments' % str(nbtab.id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def file_upload_nbreview(request, review_id,**kwargs):
    user = request.user
    profile = user.userprofile
    review = NotebooksTab_Reviews.objects.get(id=review_id)

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/notebooks_tab/show/"
#        return render(request, 'error.html', locals())

    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        review_attachment, created = NotebooksTabReviewAttachment.objects.get_or_create(review=review, attachment=new_file,
                                                                            the_name=new_file.name, user=user,
                                                                            the_size=new_file.size)
    url = '/notebooks_tab/show_nb_review/%s/#attachments' % str(review.id)
    return HttpResponseRedirect(url)


@login_required
@apply_perms
def delete_review_attachment(request, obj_id,**kwargs):
    user = request.user
    attachment = get_object_or_404(NotebooksTabReviewAttachment, id=obj_id)
    r = attachment.review
    review_id = r.id
    attachments = NotebooksTabReviewAttachment.objects.filter(review=r)
    profile = user.userprofile

    try:
#        if attachment.user == user or profile.user_type == "SUPER":
        attachment.delete()
        url = '/notebooks_tab/show_nb_review/%s/#attachments' % str(r.id)
        return HttpResponseRedirect(url)
#        else:
#            error = "You are not authorized to delete this attachment."
    except:
        error = "Failed to delete attachment. Please try again."
    print(error)

    return render(request, 'show/show_nb_review.html', locals())


@login_required
@apply_perms
def switch_is_review_file_flag_nb(request, obj_id,**kwargs):
    user = request.user
    nb_attachment = get_object_or_404(NotebooksTabAttachment, id=obj_id)

    if nb_attachment.is_review_file != "Y":
        nb_attachment.is_review_file = "Y"
    else:
        nb_attachment.is_review_file = "N"

    nb_attachment.save()

    url = '/notebooks_tab/show/%s/#attachments' % str(nb_attachment.nbtab_id)

    return HttpResponseRedirect(url)

@login_required
@apply_perms
def switch_file_email_flag_nb(request, obj_id,**kwargs):
    user = request.user
    nb_attachment = get_object_or_404(NotebooksTabAttachment, id=obj_id)

    if nb_attachment.include_in_email != "Y":
        nb_attachment.include_in_email = "Y"
    else:
        nb_attachment.include_in_email = "N"

    nb_attachment.save()

    url = '/notebooks_tab/show/%s/#attachments' % str(nb_attachment.nbtab_id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def delete_nbtab_attachment(request, obj_id,**kwargs):
    user = request.user
    nb_attachment = get_object_or_404(NotebooksTabAttachment, id=obj_id)
    nb = nb_attachment.nbtab
    nb_tab_id = nb.id

    profile = user.userprofile
    obj = get_object_or_404(NotebooksTab, id=nb_tab_id)

    nb_attachments = NotebooksTabAttachment.objects.filter(nbtab=obj)

    try:
#        if nb_attachment.user == user or profile.user_type == "SUPER":
        nb_attachment.delete()
        # url = '/notebooks_tab/show/%s/#attachments' % str(nb_attachment.nbtab_id)
        url = '/notebooks_tab/show/%s/#attachments' % str(nb_attachment.nbtab_id)
        return HttpResponseRedirect(url)
#        else:
#            error = "You are not authorized to delete this attachment."
    except:
        error = "Failed to delete attachment. Please try again."

    return render(request, 'show/show_nb_tab_item.html', locals())

@login_required
@apply_perms
def switch_is_review_file_flag_nb_review(request, obj_id,**kwargs):
    user = request.user
    nb_attachment = get_object_or_404(NotebooksTabReviewAttachment, id=obj_id)

    if nb_attachment.is_review_file != "Y":
        nb_attachment.is_review_file = "Y"
    else:
        nb_attachment.is_review_file = "N"

    nb_attachment.save()

    referer = request.META.get('HTTP_REFERER')
    url = referer + '#review_attachments'
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def switch_file_email_flag_nb_review(request, obj_id,**kwargs):
    user = request.user
    nb_attachment = get_object_or_404(NotebooksTabReviewAttachment, id=obj_id)

    if nb_attachment.include_in_email != "Y":
        nb_attachment.include_in_email = "Y"
    else:
        nb_attachment.include_in_email = "N"

    nb_attachment.save()

    referer = request.META.get('HTTP_REFERER')
    url = referer + '#review_attachments'
    return HttpResponseRedirect(url)

class NBTabEditView(FormView):

    form_class = NotebooksTabFormAsync

    template = 'main/edit_nb_tab_item.html'

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id,**kwargs):

        obj = get_object_or_404(NotebooksTab, id=obj_id)

        form = self.form_class(instance=obj)

        user = request.user

        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)
        label_class = "col-sm-4"
        input_container_class = "col-sm-8"
        no_branches = False
        office_required = True
        lab_required = True
        division_required = True

        selected_office = obj.office
        selected_lab = obj.lab
        selected_division = obj.division
        selected_branch = obj.branch

        nb_approval_history = NotebooksTab_approval_history.objects.filter(nbtab=obj)

        return render(request, self.template, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, obj_id,**kwargs):

        user = request.user
        obj = get_object_or_404(NotebooksTab, id=obj_id)

        # get the organization data
        office_list = oq.get_office_list(user, as_json=True)
        lab_list = oq.get_lab_list(user, None, as_json=True)
        division_list = oq.get_division_list(user, None, None, as_json=True)
        branch_list = oq.get_branch_list(user, None, None, None, as_json=True)
        label_class = "col-sm-4"
        input_container_class = "col-sm-8"
        no_branches = False
        office_required = True
        lab_required = True
        division_required = True

        # This needs to be up here because the values change later in the function.
        selected_office = obj.office
        selected_lab = obj.lab
        selected_division = obj.division
        selected_branch = obj.branch
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        form = self.form_class(data=request.POST, files=request.FILES, instance=obj)

        before_custodian = obj.custodian
        before_qa_manager = obj.qa_manager
        before_status = obj.status
        update_comments = request.POST.get("update_comment")

        if form.is_valid():

            nbtab = form.save(commit=False)

            org_changed = False
            if selected_office != nbtab.office:
                org_changed = True
            elif selected_lab != nbtab.lab:
                org_changed = True
            elif selected_division != nbtab.division:
                org_changed = True
            elif selected_branch != nbtab.branch:
                org_changed = True

            if org_changed:
                # rebuild Notebook Number
                lab_code = "H" if nbtab.lab.designation_code is None else str(nbtab.lab.designation_code)
                nb_prefix = lab_code + "-" + str(nbtab.division.abbreviation)
                if nbtab.branch:
                    nb_prefix += "-" + str(nbtab.branch.abbreviation)

                nbtab.nb_number = nb_prefix + "-NB-" + str(nbtab.id)


            #if the status is not active, we need to unrequest any reviews that were requested.
            if request.POST.get('status') != 1:
                scheduled_reviews = NotebooksTab_Schedule_Review.objects.filter(nbtab=nbtab)
                for sr in scheduled_reviews:
                    sr.schedule_review = 'N'
                    sr.save()

            nbtab.save()
            form.save_m2m()

            log_hist = False
            if before_custodian != nbtab.custodian:
                log_hist = True
            elif before_qa_manager != nbtab.qa_manager:
                log_hist = True
            elif before_status != nbtab.status:
                log_hist = True
            elif update_comments:
                log_hist = True

            if log_hist:
                # add to approval history
                nb_approval_history = NotebooksTab_approval_history.objects.create(nbtab=obj,
                                                                         user=user,
                                                                         custodian=obj.custodian,
                                                                         qa_manager=obj.qa_manager,
                                                                         status=obj.status,
                                                                         comments=update_comments)

            url = '/notebooks_tab/show/%s/' % str(nbtab.id)
            return HttpResponseRedirect(url)
        else:
            # Missing required fields. Need to set the local variables needed for
            # organization_select.html and discipline_select.html.
            # Grab ids from form. If they exist, get the objects and set the variables.
            selected_office_id = request.POST.get("office", None)
            if selected_office_id:
                selected_office = get_object_or_404(Office, id=selected_office_id)
                selected_lab_id = request.POST.get("lab", None)
                if selected_lab_id:
                    selected_lab = get_object_or_404(Lab, id=selected_lab_id)
                    selected_division_id = request.POST.get("division", None)
                    if selected_division_id:
                        selected_division = get_object_or_404(Division, id=selected_division_id)
                        selected_branch_id = request.POST.get("branch", None)
                        if selected_branch_id:
                            selected_branch = get_object_or_404(Branch, id=selected_branch_id)
                        else:
                            selected_branch = None
                    else:
                        selected_division = None
                else:
                    selected_lab = None
            else:
                selected_office = None

            return render(request, self.template, locals())


class CreateOrgLink_NB(FormView):
    template = "main/link_organization_nb.html"

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

            org_link = NotebooksTab_Orgs()
            nbtab = get_object_or_404(NotebooksTab, id=obj_id)
            org_link.nbtab = nbtab

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

            url = '/notebooks_tab/show/%s/#relatedorgs' % str(obj_id)
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
def delete_nb_org(request, obj_id,**kwargs):
    user = request.user
    nb_org = get_object_or_404(NotebooksTab_Orgs, id=obj_id)

#    if user.is_staff:
    nb_org.delete()

    url = '/notebooks_tab/show/%s/#relatedorgs' % str(nb_org.nbtab_id)
    return HttpResponseRedirect(url)

@login_required
@apply_perms
def search_nb_tab(request,**kwargs):
    user = request.user

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office2 = user.userprofile.office
    selected_lab2 = user.userprofile.lab
    selected_division2 = user.userprofile.division

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    notebook_statuses = NotebooksTab_NotebookStatus.objects.all().order_by('sort_number')
    nb_statuses = NotebooksTab_Status.objects.all().order_by('sort_number')
    nb_types = NotebooksTab_Type.objects.all().order_by('sort_number')
    external_orgs = ParticipatingOrganization.objects.all()
    projects = Project.objects.all().order_by('qa_id')
    programs = Program.objects.all().order_by('the_name')

    return render(request, 'main/search_nb_tab.html', locals())

@login_required
@apply_perms
def result_search_nb_tab(request,**kwargs):
    user = request.user

    # objs = NotebooksTab.objects.all()
    # the_count = len(objs)

    query = Q()
    query_show = ''
    the_count = 0

    if request is None:
        return NotebooksTab.objects.get(id=1)

    # Lead Organization
    lead_office_id = request.GET.get("office2", None)
    lead_lab_id = request.GET.get("lab2", None)
    lead_division_id = request.GET.get("division2", None)
    lead_branch_id = request.GET.get("branch2", None)

    if lead_office_id is not None and lead_office_id != '':
        lead_office = Office.objects.get(id=lead_office_id)
        query = query & (Q(office_id=lead_office_id))
        query_show = query_show + "Lead Office = " + lead_office.abbreviation + ", "

        if lead_lab_id is not None and lead_lab_id != '':
            lead_lab = Lab.objects.get(id=lead_lab_id)
            query = query & (Q(lab_id=lead_lab_id))
            query_show = query_show + "Lead Center = " + lead_lab.abbreviation + ", "

            if lead_division_id is not None and lead_division_id != '':
                lead_division = Division.objects.get(id=lead_division_id)
                query = query & (Q(division_id=lead_division_id))
                query_show = query_show + "Lead Division = " + lead_division.abbreviation + ", "

                if lead_branch_id is not None and lead_branch_id != '':
                    lead_branch = Branch.objects.get(id=lead_branch_id)
                    query = query & (Q(branch_id=lead_branch_id))
                    query_show = query_show + "Lead Branch = " + lead_branch.abbreviation + ", "

    if 'nb_number' in request.GET:
        nb_number = request.GET['nb_number']
        nb_number = nb_number.strip()  # Trim white space
        if nb_number:
            query = query & (Q(nb_number__icontains=nb_number))
            query_show = query_show + "Notebook Number = " + str(nb_number) + " "

    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            query = query & (Q(title__icontains=title))
            query_show = query_show + "Full Title = " + str(title) + " "

    if 'alt_id' in request.GET:
        alt_id = request.GET['alt_id']
        alt_id = alt_id.strip()  # Trim white space
        if alt_id:
            query = query & (Q(alt_id__icontains=alt_id))
            query_show = query_show + "Alternate ID = " + str(alt_id) + " "

    if 'previous_id' in request.GET:
        previous_id = request.GET['previous_id']
        previous_id = previous_id.strip()  # Trim white space
        if previous_id:
            query = query & (Q(previous_id__icontains=previous_id))
            query_show = query_show + "Previous ID = " + str(previous_id) + " "

    # Review Status
    item_01 = ''
    sub_query_01 = Q()
    sub_query_show_01 = ''
    if 'nb_status' in request.GET:
        nb_status = request.GET.getlist('nb_status')
        if nb_status:
            for item_01 in nb_status:
                a_status = NotebooksTab_Status.objects.get(id=item_01)
                sub_query_01 = sub_query_01 | Q(nb_status_id=item_01)
                sub_query_show_01 = sub_query_show_01 + a_status.the_name + ", "

            query = sub_query_01 & query
            query_show = query_show + "Notebook Review Status(es) => " + sub_query_show_01

    # Notebook Type
    item_02 = ''
    sub_query_02 = Q()
    sub_query_show_02 = ''
    if 'nb_type' in request.GET:
        nb_type = request.GET.getlist('nb_type')
        if nb_type:
            for item_02 in nb_type:
                a_type = NotebooksTab_Type.objects.get(id=item_02)
                sub_query_02 = sub_query_02 | Q(nb_type_id=item_02)
                sub_query_show_02 = sub_query_show_02 + a_type.the_name + ", "

            query = sub_query_02 & query
            query_show = query_show + "Notebook Type(s) => " + sub_query_show_02

    # Status
    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'notebook_status' in request.GET:
        status = request.GET.getlist('notebook_status')
        if status:
            for item_03 in status:
                b_status = NotebooksTab_NotebookStatus.objects.get(id=item_03)
                sub_query_03 = sub_query_03 | Q(status_id=item_03)
                sub_query_show_03 = sub_query_show_03 + b_status.the_name + ", "

            query = sub_query_03 & query
            query_show = query_show + "Status(es) => " + sub_query_show_03


    # Show only the notebooks that have a review requested for at least one of its custodian/contributors.
    if 'show_review_requested' in request.GET:
        show_review_requested = request.GET['show_review_requested']
        if show_review_requested:
            # Get a list of all the notebook ids of notebooks with reviews requested.
            nb_scheduled = []
            scheduledReviewRecords = NotebooksTab_Schedule_Review.objects.filter(Q(schedule_review='Y'))
            for scheduledRec in scheduledReviewRecords:
                if scheduledRec.schedule_review == 'Y' and scheduledRec.nbtab_id not in nb_scheduled:
                    nb_scheduled.append(scheduledRec.nbtab_id)

            query = query & (Q(id__in=nb_scheduled))
            query_show = query_show + "has review requested, "


    # People searches

    # Check if user has entered name data for custodian/contributor
    if 'person_last' in request.GET:
        person_last = request.GET['person_last']
    if 'person_first' in request.GET:
        person_first = request.GET['person_first']

    if 'roles' in request.GET and (person_last or person_first):

        checked_roles = request.GET.getlist('roles')
        person_criteria_list = []
        custodian_query = None;
        contributor_query = None;
        if "custodian" in checked_roles:
            custodian_query = Q()
            custodian_criteria_list = []
            if person_last:
                custodian_query = custodian_query & (Q(custodian__last_name__istartswith=person_last))
                custodian_criteria_list.append("Custodian Last Name starts with " + str(person_last))

            if person_first:
                custodian_query = custodian_query & (Q(custodian__first_name__istartswith=person_first))
                custodian_criteria_list.append("Custodian First Name starts with " + str(person_first))

            custodian_criteria = ' and '.join(custodian_criteria_list)
            person_criteria_list.append(custodian_criteria)

        if "contributor" in checked_roles:
            contributor_query = Q()
            contributor_criteria_list = []
            if person_last:
                contributor_query = contributor_query & (Q(ord_contributors__last_name__istartswith=person_last))
                contributor_criteria_list.append("ORD Contributor Last Name starts with " + str(person_last))

            if person_first:
                contributor_query = contributor_query & (Q(ord_contributors__first_name__istartswith=person_first))
                contributor_criteria_list.append("ORD Contributor First Name starts with " + str(person_first))

            contributor_criteria = ' and '.join(contributor_criteria_list)
            person_criteria_list.append(contributor_criteria)

        if contributor_query and custodian_query:
            query = query & ( custodian_query | contributor_query )
        elif custodian_query:
            query = query & custodian_query
        elif contributor_query:
            query = query & contributor_query

        query_show += '( ' + ' or '.join(person_criteria_list) + ' ) '

        # else no checked roles so ignore custodian/contributor


    if 'non_ord_contrib' in request.GET:
        non_ord_contrib = request.GET['non_ord_contrib']
        if non_ord_contrib:
            query = query & (Q(non_ord_contributors__icontains=non_ord_contrib))
            query_show = query_show + "Non-ORD Contributor Email = " + str(non_ord_contrib) + " "

    if 'qa_manager_last' in request.GET:
        qa_manager_last = request.GET['qa_manager_last']
        if qa_manager_last:
            query = query & (Q(qa_manager__last_name__istartswith=qa_manager_last))
            query_show = query_show + "QA Manager Last Name starts with " + str(qa_manager_last) + " "

    if 'qa_manager_first' in request.GET:
        qa_manager_first = request.GET['qa_manager_first']
        if qa_manager_first:
            query = query & (Q(qa_manager__first_name__istartswith=qa_manager_first))
            query_show = query_show + "QA Manager First Name starts with " + str(qa_manager_first) + " "

    if 'supervisor_mentor_last' in request.GET:
        supervisor_mentor_last = request.GET['supervisor_mentor_last']
        if supervisor_mentor_last:
            query = query & (Q(supervisor_mentor__last_name__istartswith=supervisor_mentor_last))
            query_show = query_show + "QA Manager Last Name starts with " + str(supervisor_mentor_last) + " "

    if 'supervisor_mentor_first' in request.GET:
        supervisor_mentor_first = request.GET['supervisor_mentor_first']
        if supervisor_mentor_first:
            query = query & (Q(supervisor_mentor__first_name__istartswith=supervisor_mentor_first))
            query_show = query_show + "QA Manager First Name starts with " + str(supervisor_mentor_first) + " "

    # Dates
    if 'no_date_issued' in request.GET:
        query = query & (Q(date_issued=None))
        query_show = query_show + "No Date Issued, "
    else:
        if 'date_issued_f' in request.GET:
            date_issued_f = request.GET['date_issued_f']
            if date_issued_f:
                query = query & (Q(date_issued__gte=date_issued_f))
                query_show = query_show + "Date Approved From Date = " + str(date_issued_f) + " "
        if 'date_issued_t' in request.GET:
            date_issued_t = request.GET['date_issued_t']
            if date_issued_t:
                query = query & (Q(date_issued__lte=date_issued_t))
                query_show = query_show + "Date Approved To Date = " + str(date_issued_t) + " "

    if 'no_date_final_use' in request.GET:
        query = query & (Q(date_final_use=None))
        query_show = query_show + "No Date of Final Use, "
    else:
        if 'date_final_use_f' in request.GET:
            date_final_use_f = request.GET['date_final_use_f']
            if date_final_use_f:
                query = query & (Q(date_final_use__gte=date_final_use_f))
                query_show = query_show + "Date of Final Use From Date = " + str(date_final_use_f) + " "
        if 'date_final_use_t' in request.GET:
            date_final_use_t = request.GET['date_final_use_t']
            if date_final_use_t:
                query = query & (Q(date_final_use__lte=date_final_use_t))
                query_show = query_show + "Date of Final Use To Date = " + str(date_final_use_t) + " "

    if 'no_date_archived' in request.GET:
        query = query & (Q(date_archived=None))
        query_show = query_show + "No Date Archived, "
    else:
        if 'date_archived_f' in request.GET:
            date_archived_f = request.GET['date_archived_f']
            if date_archived_f:
                query = query & (Q(date_archived__gte=date_archived_f))
                query_show = query_show + "Date Archived From Date = " + str(date_archived_f) + " "
        if 'date_archived_t' in request.GET:
            date_archived_t = request.GET['date_archived_t']
            if date_archived_t:
                query = query & (Q(date_archived__lte=date_archived_t))
                query_show = query_show + "Date Archived To Date = " + str(date_archived_t) + " "

    # Notebooks can be associated with multiple projects.
    # Search for Notebooks linked to this project ID.
    if 'project_id' in request.GET:
        project_id = request.GET['project_id']
        if project_id:
            query = query & (Q(projects__qa_id__icontains=project_id))
            query_show = query_show + "Project ID contains " + str(project_id) + " "

    # Programs
    item_04 = ''
    sub_query_04 = Q()
    sub_query_show_04 = ''
    if 'search_programs' in request.GET:
        search_programs = request.GET.getlist('search_programs')
        if search_programs and not (len(search_programs)==1 and search_programs[0] == ""): # do nothing if only the blank selected
            for item_04 in search_programs:
                if item_04 != "":
                    a_program = Program.objects.get(id=item_04)
                    sub_query_04 = sub_query_04 | Q(programs__id=item_04)
                    sub_query_show_04 = sub_query_show_04 + a_program.the_name + ", "

            query = sub_query_04 & query
            query_show = query_show + "Program(s) => " + sub_query_show_04

    # EPA Non-ORD Organization
    item_05 = ''
    sub_query_05 = Q()
    sub_query_show_05 = ''
    if 'external_org' in request.GET:
        external_org = request.GET.getlist('external_org')
        if external_org:
            for item_05 in external_org:
                ext_org = ParticipatingOrganization.objects.get(id=item_05)
                sub_query_05 = sub_query_05 | Q(participating_orgs__id=item_05)
                sub_query_show_05 = sub_query_show_05 + ext_org.company + ", "

            query = sub_query_05 & query
            query_show = query_show + "EPA Non-ORD Organization => " + sub_query_show_05

    # Related ORD Organizations
    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id=office_id)
        query = query & (Q(notebookstab_orgs__office_id=office_id))
        query_show = query_show + "Related ORD Office = " + str(office.abbreviation) + " "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id=lab_id)
        query = query & (Q(notebookstab_orgs__lab_id=lab_id))
        query_show = query_show + "Related ORD Center/Office = " + str(lab.abbreviation) + " "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id=division_id)
        query = query & (Q(notebookstab_orgs__division_id=division_id))
        query_show = query_show + "Related ORD Division = " + str(division.abbreviation) + " "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id=branch_id)
        query = query & (Q(notebookstab_orgs__branch_id=branch_id))
        query_show = query_show + "Related Organization Branch = " + str(branch.abbreviation) + " "

    # Comments
    if 'comments' in request.GET:
        comments = request.GET['comments']
        if comments:
            query = query & (Q(comments__icontains=comments))
            query_show = query_show + "Comments = " + str(comments) + " "

    objs = NotebooksTab.objects.filter(query).distinct()
    the_count = len(objs)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]


    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count > 0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=notebooks_searched.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            sheet = workbook.add_worksheet('Notebooks')

            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})

            sheet.write(0, 0, 'NB Number', label_format)
            sheet.write(0, 1, 'Previous ID', label_format)
            sheet.write(0, 2, 'Alternate ID', label_format)
            sheet.write(0, 3, 'Status', label_format)
            sheet.write(0, 4, 'Title', label_format)
            sheet.write(0, 5, 'Comments', label_format)
            sheet.write(0, 6, 'NB Type', label_format)

            sheet.write(0, 7, 'Lead Organization Office', label_format)
            sheet.write(0, 8, 'Lead Organization Center/Office', label_format)
            sheet.write(0, 9, 'Lead Organization Division', label_format)
            sheet.write(0, 10, 'Lead Organization Branch', label_format)

            sheet.write(0, 11, 'Custodian First', label_format)
            sheet.write(0, 12, 'Custodian Last', label_format)
            sheet.write(0, 13, 'QA Manager First', label_format)
            sheet.write(0, 14, 'QA Manager Last', label_format)
            sheet.write(0, 15, 'Supervisor/Mentor First', label_format)
            sheet.write(0, 16, 'Supervisor/Mentor Last', label_format)

            sheet.write(0, 17, 'Date Issued', label_format)
            sheet.write(0, 18, 'Date of Last Review', label_format)
            sheet.write(0, 19, 'Review Status', label_format)
            sheet.write(0, 20, 'Date of Final Use', label_format)
            sheet.write(0, 21, 'Date Archived', label_format)

            sheet.write(0, 22, 'Project IDs', label_format)
            sheet.write(0, 23, 'Programs', label_format)
            sheet.write(0, 24, 'Related EPA Non-ORD Organizations', label_format)
            sheet.write(0, 25, 'Related ORD Organizations', label_format)

            sheet.write(0, 26, 'Follow-up Email List (ORD)', label_format)
            sheet.write(0, 27, 'Follow-up Email List (non-ORD)', label_format)

            sheet.write(0, 28, 'ORD Contributor List (ORD)', label_format)
            sheet.write(0, 29, 'ORD Contributor List (non-ORD)', label_format)

            i = 0
            for obj in objs:

                recent_review = NotebooksTab_Reviews.objects.filter(nbtab=obj).order_by('-date_reviewed').first()
                if recent_review is not None:
                    date_reviewed = recent_review.date_reviewed if recent_review.date_reviewed is not None else ""
                    review_status = recent_review.status if recent_review.status is not None else ""
                else:
                    date_reviewed = ""
                    review_status = ""

                i += 1
                sheet.write(i, 0, obj.nb_number)
                sheet.write(i, 1, obj.previous_id)
                sheet.write(i, 2, obj.alt_id)

                if obj.status is not None:
                   sheet.write(i, 3, obj.status.the_name)
                else:
                    sheet.write(i, 3, '')

                sheet.write(i, 4, obj.title)
                sheet.write(i, 5, obj.comments)

                if obj.nb_type is not None:
                    sheet.write(i, 6, obj.nb_type.the_name)
                else:
                    sheet.write(i, 6, '')

                if obj.office is not None:
                    sheet.write(i, 7, obj.office.abbreviation)
                else:
                    sheet.write(i, 7, '')

                if obj.lab is not None:
                    sheet.write(i, 8, obj.lab.abbreviation)
                else:
                    sheet.write(i, 8, '')

                if obj.division is not None:
                    sheet.write(i, 9, obj.division.abbreviation)
                else:
                    sheet.write(i, 9, '')

                if obj.branch is not None:
                    sheet.write(i, 10, obj.branch.abbreviation)
                else:
                    sheet.write(i, 10, '')

                if obj.custodian is not None:
                    sheet.write(i, 11, obj.custodian.first_name)
                    sheet.write(i, 12, obj.custodian.last_name)
                else:
                    sheet.write(i, 11, '')
                    sheet.write(i, 12, '')

                if obj.qa_manager is not None:
                    sheet.write(i, 13, obj.qa_manager.first_name)
                    sheet.write(i, 14, obj.qa_manager.last_name)
                else:
                    sheet.write(i, 13, '')
                    sheet.write(i, 14, '')

                if obj.supervisor_mentor is not None:
                    sheet.write(i, 15, obj.supervisor_mentor.first_name)
                    sheet.write(i, 16, obj.supervisor_mentor.last_name)
                else:
                    sheet.write(i, 15, '')
                    sheet.write(i, 16, '')

                sheet.write(i, 17, str(obj.date_issued))
                sheet.write(i, 18, str(date_reviewed))

                sheet.write(i, 19, str(review_status))

                sheet.write(i, 20, str(obj.date_final_use))
                sheet.write(i, 21, str(obj.date_archived))

                # Combine any project ids into one string
                if obj.projects is not None:
                    projects = obj.projects.all()
                    project_ids = ''
                    for proj in projects:
                        if project_ids == '':
                            project_ids = proj.qa_id
                        else:
                            project_ids = project_ids + ';' + proj.qa_id
                    sheet.write(i, 22, project_ids)
                else:
                    sheet.write(i, 22, '')

                # Combine any programs into one string
                if obj.programs is not None:
                    programs = obj.programs.all()
                    programs_str = ''
                    for prog in programs:
                        if programs_str == '':
                            programs_str = prog.the_name
                        else:
                            programs_str = programs_str + ';' + prog.the_name
                    sheet.write(i, 23, programs_str)
                else:
                    sheet.write(i, 23, '')

                # EPA Non-ORD Organizations
                # Combine any EPA non-ORD organizations into one string
                if obj.participating_orgs is not None:
                    participating_orgs = obj.participating_orgs.all()
                    partic_orgs_str = ''
                    for an_org in participating_orgs:
                        if partic_orgs_str == '':
                            partic_orgs_str = an_org.company
                        else:
                            partic_orgs_str = partic_orgs_str + ';' + an_org.company
                    sheet.write(i, 24, partic_orgs_str)
                else:
                    sheet.write(i, 24, '')

                # ORD Organizations
                orgs = NotebooksTab_Orgs.objects.filter(nbtab=obj)
                related_orgs = ''
                for an_org in orgs:
                    if an_org.office:
                        org_name = an_org.office.abbreviation
                        if an_org.lab:
                            org_name = org_name + '-' + an_org.lab.abbreviation
                            if an_org.division:
                                org_name = org_name + '-' + an_org.division.abbreviation
                                if an_org.branch:
                                    org_name = org_name + '-' + an_org.branch.abbreviation

                    if related_orgs == '':
                        related_orgs = org_name
                    else:
                        related_orgs = related_orgs + ';' + org_name

                sheet.write(i, 25, related_orgs)

                # ORD Emails
                ord_people = ''
                for person in obj.nb_review_distribution_list.all():
                    if ord_people == '':
                        ord_people = person.email
                    else:
                        ord_people = ord_people + ';' + person.email

                sheet.write(i, 26, ord_people)

                # non-ORD Emails
                sheet.write(i, 27, obj.nb_review_email_list)

                # ORD Emails
                # the_list = []
                # if obj.ord_contributors is not None:
                #     for c in obj.ord_contributors.all():
                #         the_list += ' ' + c.last_name + ', ' + c.first_name
                #     sheet.write(i, 28, the_list)
                # else:
                #     sheet.write(i, 28, '')

                ord_people = ''
                for person in obj.ord_contributors.all():
                    if ord_people == '':
                        ord_people = person.last_name + ", " + person.first_name
                    else:
                        ord_people = ord_people + '; ' + person.last_name + ", " + person.first_name

                sheet.write(i, 28, ord_people)

                # non-ORD Emails
                sheet.write(i, 29, obj.non_ord_contributors)

            # wrap up - Add a sheet with the query
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, query_show)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response

    return render(request, 'main/search_nb_tab_result.html', locals())


@login_required
@apply_perms
def result_search_nb_periodic_review(request,**kwargs):

    user = request.user

    # because we do this a lot.
    def reqhas(value):
        return value is not None and value != ''

    def parseDate(value):
        return datetime.date(datetime.strptime(value,'%Y-%m-%d'))

    def maxOrNone(lst):
        try:
            return max(lst)
        except TypeError:
            return None
    #
    # Filter Strategy:
    # We have a model NotebooksTab_user_notebooks which relates user, notebook, review, role.
    #   1. We filter that based on parameters related to the user, notebooks and reviews
    #   2. Take the users we are left with and associate their notebooks and reviews.
    #   3. Find the last review date and last email date for the user
    #
    #


    #
    # USER FILTERS
    #

    user_query = Q()
    nb_annual_criteria = ""

    lead_office_id = request.GET.get("office", None)
    if reqhas(lead_office_id):
        user_query = user_query & Q(user__userprofile__office_id=lead_office_id)
        nb_annual_criteria += "C/C Organization = " + str(Office.objects.get(id=lead_office_id).abbreviation) + " and "

        lead_lab_id = request.GET.get("lab", None)
        if reqhas(lead_lab_id):
            user_query = user_query & Q(user__userprofile__lab_id=lead_lab_id)
            nb_annual_criteria += "C/C Center = " + str(Lab.objects.get(id=lead_lab_id).abbreviation) + " and "

            lead_division_id = request.GET.get("division", None)
            if reqhas(lead_division_id):
                user_query = user_query & Q(user__userprofile__division_id=lead_division_id)
                nb_annual_criteria += "C/C Division = " + str(Division.objects.get(id=lead_division_id).abbreviation) + " and "

                lead_branch_id = request.GET.get("branch", None)
                if reqhas(lead_branch_id):
                    user_query = user_query & Q(user__userprofile__branch_id=lead_branch_id)
                    nb_annual_criteria += "C/C Branch = " + str(Branch.objects.get(id=lead_branch_id).abbreviation) + " and "


    person_last = request.GET.get("person_last", None)
    person_first = request.GET.get("person_first", None)
    checked_roles = request.GET.getlist('roles',None)

    if len(checked_roles) or reqhas(person_last) or reqhas(person_first):

        if len(checked_roles) == 2:
            pass
        elif "custodian" in checked_roles:
            nb_annual_criteria += "Role = Custodian and "
            user_query = user_query & Q(roles__contains=['custodian'])
        elif "contributor" in checked_roles:
            nb_annual_criteria += "Role = Contributor and "
            user_query = user_query & Q(roles__contains=['contributor'])

        # Check if user has entered name data for custodian/contributor
        if person_last:
            user_query = user_query & Q(user__last_name__istartswith=person_last.strip())
            nb_annual_criteria += "Last Name starts with " + person_last + " and "
        if person_first:
            user_query = user_query & Q(user__first_name__istartswith=person_first.strip())
            nb_annual_criteria += "First Name starts with " + person_first + " and "

    # Show only the people who already have a review requested.
    show_review_requested = request.GET.get("show_review_requested", None)
    if reqhas(show_review_requested):
        # Get a list of all the user ids of users with reviews requested.
        users_scheduled = []
        scheduledReviewRecords = NotebooksTab_Schedule_Review.objects.filter(Q(schedule_review='Y'))
        for scheduledRec in scheduledReviewRecords:
            if scheduledRec.schedule_review == 'Y' and scheduledRec.user_id not in users_scheduled:
                users_scheduled.append(scheduledRec.user_id)
        user_query = user_query & Q(user__id__in=users_scheduled)
        nb_annual_criteria += "has review requested and "

    users = NotebooksTab_User_Notebooks.objects.filter(user_query)





    #
    # NOTEBOOK FILTERS
    #
    qa_manager_last = request.GET.get("qa_manager_last", None)
    qa_manager_first = request.GET.get("qa_manager_first", None)

    if reqhas(qa_manager_last) or reqhas(qa_manager_first):

        nb_query = Q()
        if reqhas(qa_manager_last):
            nb_query = nb_query & Q(qa_manager__last_name__istartswith=qa_manager_last.strip())
            nb_annual_criteria += "QA Manager Last Name starts with " + str(qa_manager_last) + " and "

        if reqhas(qa_manager_first):
            nb_query = nb_query & Q(qa_manager__first_name__istartswith=qa_manager_first.strip())
            nb_annual_criteria += "QA Manager First Name starts with " + str(qa_manager_first) + " and "

        notebooks = NotebooksTab.objects.filter(nb_query)
        nb_ids = [nb.id for nb in notebooks]
        users = users.filter(nbtab_ids__overlap=nb_ids)

    #
    # REVIEW FILTERS
    #
    review_date_f = request.GET.get("review_date_f", None)
    review_date_t = request.GET.get("review_date_t", None)
    review_status = request.GET.get("review_status", None)
    show_never_reviewed = request.GET.get("show_never_reviewed", None)
    if reqhas(review_date_f) or reqhas(review_date_t) or reqhas(review_status):
        review_query = Q()

        if reqhas(review_date_f):
            review_query = review_query & Q(recent_review__date_reviewed__gte=review_date_f)
            nb_annual_criteria += "Date of Last Review From = " + review_date_f + " and "

        if reqhas(review_date_t) and not reqhas(review_date_f) and reqhas(show_never_reviewed):
            review_query = review_query | (
                    Q(recent_review__date_reviewed__lte=review_date_t)
                    | Q(recent_review__isnull=True)
                    | Q(recent_review__date_reviewed__isnull=True)
                    | Q(recent_review__status__isnull=True)
                    | Q(recent_review__status=3)
                    )
            nb_annual_criteria += "Date of Last Review To Date = " + review_date_t + " or never reviewed and "
        elif reqhas(review_date_t):
            review_query = review_query & Q(recent_review__date_reviewed__lte=review_date_t)
            nb_annual_criteria += "Date of Last Review To Date = " + review_date_t + " and "

        if reqhas(review_status):
            if(int(review_status) == 3): #not reviewed
                review_query = review_query & ( Q(recent_review__status__pk=3) | Q(recent_review__status__isnull=True) | Q(recent_review__isnull=True))
            else:
                review_query = review_query & Q(recent_review__status__pk=review_status)
            status_name = NotebooksTab_Status.objects.get(pk=review_status).the_name
            nb_annual_criteria += "Last Review Status is " + status_name + " and "

        users = users.filter(review_query).order_by('user__first_name')

    #add notebook information for each user
    for nb_user in users:

        nb_ids = [int(_id) for _id in nb_user.nbtab_ids]
        roles = dict(zip(nb_ids,nb_user.roles))
        nb_user.notebooks = NotebooksTab.objects.filter(pk__in=nb_ids)
        for nb in nb_user.notebooks:
            if nb_ids.count(nb.id) > 1:
                nb.role = 'Custodian-Contributor'
            else:
                nb.role = roles[nb.id].capitalize()

            nb.sr = NotebooksTab_Schedule_Review.objects.filter(nbtab=nb,user=nb_user.user).first()

        a_year_ago = timezone.now().date() - timedelta(days=365)
        has_active_notebooks = False
        #A user doesn't need review if they have no active notebooks
        for nb in nb_user.notebooks:
            if nb.status_id == 1:
                has_active_notebooks = True

        try:
            nb_user.needs_review = 'N' if ( not has_active_notebooks or nb_user.recent_review.date_reviewed > a_year_ago ) else 'Y'
        except AttributeError:
            nb_user.needs_review = 'Y'


    if nb_annual_criteria != "":
        nb_annual_criteria = nb_annual_criteria[:-5]
    else:
        nb_annual_criteria="no criteria"



    if 'excel' in request.GET and len(users) > 0:
        excel = request.GET['excel']
        if excel == "Y":

            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=NotebookCustodiansContributorsNeedingReview.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            worksheet = workbook.add_worksheet('Notebook Reviews')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "Notebook Custodians and Contributors", section_format)

            row += 1
            today = datetime.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "C/C First Name", label_format)
            worksheet.write(row, 1, "C/C Last Name", label_format)
            worksheet.write(row, 2, "C/C Email", label_format)
            worksheet.write(row, 3, "C/C Office", label_format)
            worksheet.write(row, 4, "C/C Center/Office", label_format)
            worksheet.write(row, 5, "C/C Division", label_format)
            worksheet.write(row, 6, "C/C Branch", label_format)
            worksheet.write(row, 7, "C/C Needs Review", label_format)
            worksheet.write(row, 8, "Notebook", label_format)
            worksheet.write(row, 9, "Date Last Reviewed", label_format)
            worksheet.write(row, 10, "Last Review Status", label_format)
            worksheet.write(row, 11, "Email Last Sent", label_format)
            worksheet.write(row, 12, "Notebook Office", label_format)
            worksheet.write(row, 13, "Notebook Center/Office", label_format)
            worksheet.write(row, 14, "Notebook Division", label_format)
            worksheet.write(row, 15, "Notebook Branch", label_format)
            worksheet.write(row, 16, "Notebook Type", label_format)
            worksheet.write(row, 17, "Previous ID", label_format)
            worksheet.write(row, 18, "Alternative ID", label_format)
            worksheet.write(row, 19, "Title", label_format)
            worksheet.write(row, 20, "Role", label_format)
            worksheet.write(row, 21, "Supervisor or Mentor", label_format)
            worksheet.write(row, 22, "QA Manager", label_format)
            worksheet.write(row, 23, "Review Requested", label_format)
            worksheet.write(row, 24, "Notebook Custodian", label_format)
            worksheet.write(row, 25, "Notebook ORD Contributors", label_format)

            for user in users:
                for notebook in user.notebooks:
                    row += 1

                    user_office = user.user.userprofile.office.abbreviation if user.user.userprofile.office else ""
                    user_lab = user.user.userprofile.lab.abbreviation if user.user.userprofile.lab else ""
                    user_division = user.user.userprofile.division.abbreviation if user.user.userprofile.division else ""
                    user_branch = user.user.userprofile.branch.abbreviation if user.user.userprofile.branch else ""

                    worksheet.write(row, 0, user.user.first_name)
                    worksheet.write(row, 1, user.user.last_name)
                    worksheet.write(row, 2, user.user.email)
                    worksheet.write(row, 3, user_office)
                    worksheet.write(row, 4, user_lab)
                    worksheet.write(row, 5, user_division)
                    worksheet.write(row, 6, user_branch)
                    worksheet.write(row, 7, user.needs_review)


                    nb_office = notebook.office.abbreviation if notebook.office  else ''
                    nb_lab = notebook.lab.abbreviation if notebook.lab  else ''
                    nb_division = notebook.division.abbreviation if notebook.division  else ''
                    nb_branch = notebook.branch.abbreviation if notebook.branch  else ''
                    nb_supervisor = notebook.supervisor_mentor.userprofile.full_name if notebook.supervisor_mentor  else ''
                    nb_qam = notebook.qa_manager.userprofile.full_name if notebook.qa_manager  else ''
                    schedule_review = notebook.sr.schedule_review if notebook.sr else 'N'
                    nb_custodian = notebook.custodian.userprofile.full_name if notebook.custodian  else ''

                    nb_last_review = NotebooksTab_Reviews.objects.filter(nbtab=notebook,user=user.user).order_by('-date_reviewed').first()
                    if nb_last_review is not None:
                        date_reviewed = nb_last_review.date_reviewed if nb_last_review.date_reviewed is not None else ""
                        review_status = nb_last_review.status if nb_last_review.status is not None else ""
                    else:
                        date_reviewed = ""
                        review_status = ""

                    if date_reviewed != "":
                        print(date_reviewed)

                    nb_sched_review = NotebooksTab_Schedule_Review.objects.filter(nbtab=notebook,user=user.user).first()
                    if nb_sched_review is not None:
                        email_last_sent = nb_sched_review.email_last_sent if nb_sched_review.email_last_sent is not None else ""
                        schedule_review = nb_sched_review.schedule_review if nb_sched_review.schedule_review is not None else "N"
                    else:
                        email_last_sent = ""
                        schedule_review = "N"

                    ord_people_list = []
                    for person in notebook.ord_contributors.all():
                        ord_people_list.append(person.userprofile.full_name)
                    ord_people = ', '.join(ord_people_list)

                    worksheet.write(row, 8, notebook.nb_number)
                    worksheet.write(row, 9, str(date_reviewed))
                    worksheet.write(row, 10, str(review_status))
                    worksheet.write(row, 11, str(email_last_sent))
                    worksheet.write(row, 12, nb_office)
                    worksheet.write(row, 13, nb_lab)
                    worksheet.write(row, 14, nb_division)
                    worksheet.write(row, 15, nb_branch)
                    worksheet.write(row, 16, str(notebook.nb_type))
                    worksheet.write(row, 17, notebook.previous_id)
                    worksheet.write(row, 18, notebook.alt_id)
                    worksheet.write(row, 19, notebook.title)
                    worksheet.write(row, 20, notebook.role)
                    worksheet.write(row, 21, nb_supervisor)
                    worksheet.write(row, 22, nb_qam)
                    worksheet.write(row, 23, schedule_review)
                    worksheet.write(row, 24, nb_custodian)
                    worksheet.write(row, 25, ord_people)


            # Add a sheet with the query so user knows if these have been filtered by org and/or person.
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, nb_annual_criteria)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response


    return render(request, 'list/list_annual_nb_review.html', locals())


@login_required
@apply_perms
def nbtab_nb_review(request, nb_id,**kwargs):
    nb_id = int(nb_id)
    nb = NotebooksTab.objects.get(pk=nb_id)
    nb.reviews = NotebooksTab_Reviews.objects.filter(nbtab_id=nb_id)
    users = NotebooksTab_User_Notebooks.objects.filter(nbtab_ids__contains=[nb_id])
    show_nb_review = True
    for user in users:
        nb_ids = list(user.nbtab_ids)
        roles = list(user.roles)
        user.this_nb_review = nb.reviews.filter(user_id=user.user_id,nbtab_id=nb_id).first()
        user.sr = NotebooksTab_Schedule_Review.objects.filter(nbtab=nb,user=user.user).first()

        if nb_ids.count(nb_id) > 1:
            role = 'Custodian/Contributor'
        else:
            role = roles[nb_ids.index(nb_id)].capitalize()
        user.role = role

        a_year_ago = timezone.now().date() - timedelta(days=365)

    return render(request, 'main/nb_reviews.html', locals())


@login_required
@apply_perms
def nbtab_user_review(request, user_id,**kwargs):
    user = request.user

#    user = NotebooksTab_User_Notebooks.objects.filter(user_id=user_id).first()
    nb_user = get_object_or_404(NotebooksTab_User_Notebooks, user_id=user_id)
    nb_ids = [int(_id) for _id in nb_user.nbtab_ids]
    roles = dict(zip(nb_ids,nb_user.roles))
    notebooks = NotebooksTab.objects.filter(pk__in=nb_ids)
    nb_user.reviews = NotebooksTab_Reviews.objects.filter(user=nb_user.user_id)
    show_user_review = True


    a_year_ago = timezone.now().date() - timedelta(days=360)
    has_active_notebooks = False


    if notebooks:
        for nb in notebooks:
            if nb_ids.count(nb.id) > 1:
                nb.role = 'Custodian/Contributor'
            else:
                nb.role = roles[nb.id].capitalize()
            nb_review = NotebooksTab_Reviews.objects.filter(user_id=nb_user.user_id,nbtab_id=nb.id).first()
            nb.review = nb_review
            nb.sr = NotebooksTab_Schedule_Review.objects.filter(nbtab_id=nb.id,user_id=user_id).first()

            if nb.status_id == 1:
                has_active_notebooks = True

    try:
        nb_user.needs_review = 'N' if ( not has_active_notebooks or nb_user.recent_review.date_reviewed > a_year_ago ) else 'Y'
    except AttributeError:
        nb_user.needs_review = 'Y'

    nb_user.notebooks = notebooks

    return render(request, 'main/user_reviews.html', locals())


class nbtab_create_nb_review(FormView):

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, user_id,nb_id,**kwargs):

        form = NotebooksTabReviewFormAsync(user_id=user_id,nb_id=nb_id)
        return render(request, 'main/create_nb_review.html', locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, user_id, nb_id, *args, **kwargs):

        form = NotebooksTabReviewFormAsync(user_id=user_id,nb_id=nb_id, data=request.POST)

        if form.is_valid():
            nbtab_id = request.POST.get('notebook')
            nb_user = request.POST.get('nb_user')
            status_id = request.POST.get('status')
            date_reviewed = datetime.date(datetime.strptime(request.POST.get('date_reviewed') ,'%Y-%m-%d'))
            reviewer = request.POST.get('reviewer')
            comments = request.POST.get('comments',None)

            review_rec = NotebooksTab_Reviews()
            review_rec.nbtab_id = nbtab_id
            review_rec.user_id = nb_user
            review_rec.created = datetime.today()
            review_rec.status_id = status_id
            review_rec.date_reviewed = date_reviewed
            review_rec.reviewer_id = reviewer
            review_rec.comments = comments

            review_rec.save()

            #
            # Set schedule_review record to N
            #
            schedule_review_rec = NotebooksTab_Schedule_Review.objects.filter(user_id=nb_user,nbtab_id=nbtab_id).first()
            if schedule_review_rec is None:
                schedule_review_rec = NotebooksTab_Schedule_Review()
                schedule_review_rec.user_id = nb_user
                schedule_review_rec.nbtab_id = nbtab_id

            schedule_review_rec.schedule_review = 'N'

            schedule_review_rec.save()


            return HttpResponseRedirect('/notebooks_tab/show_nb_review/' + str(review_rec.id))
        else:

            return render(request, 'main/create_nb_review.html', locals())

class nbtab_edit_nb_review(FormView):

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, review_id,**kwargs):

        r = get_object_or_404(NotebooksTab_Reviews, id=review_id)
        print(r.user_id,r.nbtab_id)
        form = NotebooksTabReviewFormAsync(user_id=r.user_id,nb_id=r.nbtab_id, instance=r, editing=True)
        return render(request, 'main/edit_nb_review.html', locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, review_id, *args, **kwargs):

        r = get_object_or_404(NotebooksTab_Reviews, id=review_id)
        form = NotebooksTabReviewFormAsync(user_id=r.user_id,nb_id=r.nbtab_id, data=request.POST, editing=True)

        if form.is_valid():
            status_id = request.POST.get('status')
            date_reviewed = datetime.date(datetime.strptime(request.POST.get('date_reviewed') ,'%Y-%m-%d'))
            reviewer = request.POST.get('reviewer')
            comments = request.POST.get('comments',None)

            review_rec = r
            review_rec.created = datetime.today()
            review_rec.status_id = status_id
            review_rec.date_reviewed = date_reviewed
            review_rec.reviewer_id = reviewer
            review_rec.comments = comments

            review_rec.save()

            #
            # Set schedule_review record to N
            #
            nb_user = r.user
            nbtab = r.nbtab
            schedule_review_rec = NotebooksTab_Schedule_Review.objects.filter(user=nb_user,nbtab=nbtab).first()
            if schedule_review_rec is None:
                schedule_review_rec = NotebooksTab_Schedule_Review()
                schedule_review_rec.user_id = nb_user.id
                schedule_review_rec.nbtab_id = nbtab.id

            schedule_review_rec.schedule_review = 'N'

            schedule_review_rec.save()


            return HttpResponseRedirect('/notebooks_tab/show_nb_review/' + str(review_rec.id))
        else:

            return render(request, 'main/edit_nb_review.html', locals())



@apply_perms
def show_nb_review(request, review_id,**kwargs):

    show_review_edit = True
    r = get_object_or_404(NotebooksTab_Reviews, id=review_id)
    attachments = NotebooksTabReviewAttachment.objects.filter(review=r)
    return render(request, 'show/show_nb_review.html', locals())


class nbtab_set_sched_review(FormView):

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, user_id,nb_id, scrollto='',**kwargs):
        referer = self.request.META.get('HTTP_REFERER')
        schedule_review_rec = NotebooksTab_Schedule_Review.objects.filter(user_id=user_id,nbtab_id=nb_id).first()
        if schedule_review_rec is None:
            schedule_review_rec = NotebooksTab_Schedule_Review()
            schedule_review_rec.user_id = user_id
            schedule_review_rec.nbtab_id = nb_id
            schedule_review_rec.schedule_review = 'Y'

            # Send email notification.

        else:
            if schedule_review_rec.schedule_review == 'N':
                schedule_review_rec.schedule_review = 'Y'

                # Send email notification.

            else:
                schedule_review_rec.schedule_review = 'N'


        # If just requested a review, send notification.
        if schedule_review_rec.schedule_review == 'Y':
            support_email = settings.DEFAULT_QATRACK_EMAIL
            myos = platform.system()
            if myos == 'Darwin' or myos == 'Windows':  # On local dev
                print('Getting local html file.')
                html_file = os.getcwd() + '/notebooks_tab/templates/nbReviewRequest.txt'
            else:  # We're on linux
                html_file = '/var/www/html/qatrack/notebooks_tab/templates/nbReviewRequest.txt'

            plaintext = get_template(html_file)

            to_emails = []
            user = schedule_review_rec.user
            qam = schedule_review_rec.nbtab.qa_manager
            supervisor = schedule_review_rec.nbtab.supervisor_mentor
            nb = schedule_review_rec.nbtab

            to_emails.append(user.email)

            if qam is not None:
                to_emails.append(qam.email)

            if supervisor is not None:
                to_emails.append(supervisor.email)

            print("NOTEBOOK: " + nb.nb_number)
            print("EMAILING", to_emails)

            title = nb.title if nb.title is not None else ''
            safe_title = title.replace('\n', ' ').replace('\r', ' ')
            email_subject = 'Annual Notebook Review Requested for Notebook ' + nb.nb_number + ': ' + safe_title
            descr = "RE: Notebook " + nb.nb_number + ": " + title + "\r\n"

            # Include alternate and previous IDs, if any.
            if nb.alt_id:
                descr = descr + "Alternate ID: " + nb.alt_id + "\r\n"
            if nb.previous_id:
                descr = descr + "Previous ID: " + nb.previous_id + "\r\n"

            text_content = plaintext.render()
            text_content = descr + "\r\n" + text_content

            the_email = createQTEmailMessage(email_subject, text_content, support_email, to_emails)
            the_email.send(fail_silently=False)

            # update our schedule email record
            schedule_review_rec.email_last_sent = timezone.now()

        schedule_review_rec.save()

        if "show" in referer:
            referer = referer + '#users'

        return HttpResponseRedirect(referer)



#
# Legacy
#
@login_required
@apply_perms
def switch_nb_schedule_review_flag(request, obj_id, nb_annual_sql, query_show='',**kwargs):
    user = request.user
    nbtab = get_object_or_404(NotebooksTab, id=obj_id)

    if nbtab.schedule_review != "Y":
        nbtab.schedule_review = "Y"
    else:
        nbtab.schedule_review = "N"

    nbtab.save()

    # Recreate search to refresh the results page.
    objs = User.objects.raw(nb_annual_sql)

    the_count = 0
    for obj in objs:
        the_count += 1

    return render(request, 'list/list_annual_nb_review.html', locals())



@login_required
@apply_perms
def search_nb_periodic_review(request,**kwargs):
    user = request.user
    title = "Search Notebooks to Review"

    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"
    a_year_ago = datetime.now() - timedelta(days=365)
    default_date = a_year_ago.strftime('%Y-%m-%d')

    review_status = NotebooksTab_Status.objects.all()

    return render(request, 'main/search_nb_periodic_review.html', locals())


@login_required
@apply_perms
def search_nb_sepcustodian(request, **kwargs):
    user = request.user
    title = "Search Notebooks"

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

    notebook_statuses = NotebooksTab_NotebookStatus.objects.all().order_by('sort_number')

    return render(request, 'main/search_nb_sepcustodian.html', locals())

@login_required
@apply_perms
def result_search_nb_sepcustodian(request, **kwargs):
    user = request.user

    query = Q()
    query_show = ''
    the_count = 0

    title = "Search Notebooks with Separated Notebook Custodian - With Results Shown"

    if request is None:
        return NotebooksTab.objects.get(id=1)

    # Lead Organization
    office_id = request.GET.get("office", None)
    lab_id = request.GET.get("lab", None)
    division_id = request.GET.get("division", None)
    branch_id = request.GET.get("branch", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id=office_id)
        query = query & (Q(office__id=office_id))
        query_show = query_show + "Lead Office = " + str(office.abbreviation) + ", "

    if lab_id is not None and lab_id != '':
        lab = Lab.objects.get(id=lab_id)
        query = query & (Q(lab__id=lab_id))
        query_show = query_show + "Lead Center = " + str(lab.abbreviation) + ", "

    if division_id is not None and division_id != '':
        division = Division.objects.get(id=division_id)
        query = query & (Q(division__id=division_id))
        query_show = query_show + "Lead Division = " + str(division.abbreviation) + ", "

    if branch_id is not None and branch_id != '':
        branch = Branch.objects.get(id=branch_id)
        query = query & (Q(branch__id=branch_id))
        query_show = query_show + "Lead Branch = " + str(branch.abbreviation) + ", "

    # Status
    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'notebook_status' in request.GET:
        status = request.GET.getlist('notebook_status')
        if status:
            for item_03 in status:
                b_status = NotebooksTab_NotebookStatus.objects.get(id=item_03)
                sub_query_03 = sub_query_03 | Q(status_id=item_03)
                sub_query_show_03 = sub_query_show_03 + b_status.the_name + ", "

            query = sub_query_03 & query
            query_show = query_show + "Status(es) => " + sub_query_show_03

    objs = NotebooksTab.objects.filter(query).distinct()
    the_count = len(objs)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    wanted_items = set()

    for nb in objs:

        has_issue = False

        # Check if notebook custodian has separated.
        if nb.custodian is not None:
            if nb.custodian.userprofile.date_epa_separation is not None:
                today = timezone.now().date()
                if nb.custodian.userprofile.date_epa_separation <= today:
                    has_issue = True

        if has_issue == True:
            wanted_items.add(nb.pk)

    objs = objs.filter(pk__in=wanted_items)
    the_count = len(objs)

    ############
    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count > 0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=NotebooksSeparatedCustodian.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            worksheet = workbook.add_worksheet('Notebooks')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "Notebooks with Separated Notebook Custodian", section_format)

            row += 1
            today = timezone.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "Office", label_format)
            worksheet.write(row, 1, "Center", label_format)
            worksheet.write(row, 2, "Division", label_format)
            worksheet.write(row, 3, "Branch", label_format)
            worksheet.write(row, 4, "NB Number", label_format)
            worksheet.write(row, 5, 'NB Type', label_format)
            worksheet.write(row, 6, "Status", label_format)
            worksheet.write(row, 7, "Previous ID", label_format)
            worksheet.write(row, 8, "Alternate ID", label_format)
            worksheet.write(row, 9, "Title", label_format)
            worksheet.write(row, 10, "Notebook Custodian", label_format)
            worksheet.write(row, 11, "Notebook Custodian Separation Date", label_format)
            worksheet.write(row, 12, "ORD Contributors", label_format)
            worksheet.write(row, 13, "QA Manager", label_format)
            worksheet.write(row, 14, "Supervisor/Mentor", label_format)
            worksheet.write(row, 15, "Date Issued", label_format)
            worksheet.write(row, 16, "Date of Final Use", label_format)
            worksheet.write(row, 17, "Date Archived", label_format)

            for nb in objs:
                row += 1
                worksheet.write(row, 0, nb.office.abbreviation)
                if nb.lab:
                    worksheet.write(row, 1, nb.lab.abbreviation)
                else:
                    worksheet.write(row, 1, "")
                if nb.division:
                    worksheet.write(row, 2, nb.division.abbreviation)
                else:
                    worksheet.write(row, 2, "")
                if nb.branch:
                    worksheet.write(row, 3, nb.branch.abbreviation)
                else:
                    worksheet.write(row, 3, "")
                worksheet.write(row, 4, nb.nb_number)

                if nb.nb_type is not None:
                    worksheet.write(row, 5, nb.nb_type.the_name)
                else:
                    worksheet.write(row, 5, '')

                if nb.status is not None:
                   worksheet.write(row, 6, nb.status.the_name)
                else:
                    worksheet.write(row, 6, '')

                worksheet.write(row, 7, nb.previous_id)
                worksheet.write(row, 8, nb.alt_id)
                worksheet.write(row, 9, nb.title)

                worksheet.write(row, 10, nb.custodian.first_name + " " + nb.custodian.last_name)
                if nb.custodian.userprofile.date_epa_separation:
                    worksheet.write(row, 11, str(nb.custodian.userprofile.date_epa_separation))
                else:
                    worksheet.write(row, 11, "")

                ord_people = ''
                for person in nb.ord_contributors.all():
                    if ord_people == '':
                        ord_people = person.last_name + ", " + person.first_name
                    else:
                        ord_people = ord_people + '; ' + person.last_name + ", " + person.first_name

                worksheet.write(row, 12, ord_people)

                if nb.qa_manager is not None:
                    worksheet.write(row, 13, nb.qa_manager.first_name + " " + nb.qa_manager.last_name)
                else:
                    worksheet.write(row, 13, "")

                if nb.supervisor_mentor is not None:
                    worksheet.write(row, 14,
                                    nb.supervisor_mentor.first_name + " " + nb.supervisor_mentor.last_name)
                else:
                    worksheet.write(row, 14, "")

                worksheet.write(row, 15, str(nb.date_issued))
                worksheet.write(row, 16, str(nb.date_final_use))
                worksheet.write(row, 17, str(nb.date_archived))

            # wrap up - Add a sheet with the query
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, query_show)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response

    return render(request, 'main/search_nb_sepcustodian_result.html', locals())
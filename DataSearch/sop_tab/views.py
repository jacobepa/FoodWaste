from django.shortcuts import render


from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context

from django.http import Http404, HttpResponseRedirect, HttpResponse

from projects.models import *

from sop_tab.models import *

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
from time import gmtime, strftime, localtime

import xlwt

from django.http import HttpResponse  # for testing

from django.shortcuts import render, redirect

import os

# Added to handle exporting to Excel
import io
import xlsxwriter
import datetime
from datetime import datetime, timedelta

from constants.models import *

import sop_tab.query_utils as sopq

from django.core.handlers.wsgi import WSGIRequest

from constants.perms import apply_perms



@login_required
@apply_perms
def index(request,**kwargs):

    user = request.user
    title = "SOP Main Page"

    # The main SOP page displays info about the biennial reviews.
    # Get the sample email text to display.
    html_file = os.path.join(os.path.dirname(__file__), 'templates/sopReview.txt')
    f = open(html_file, 'r')

    return render(request, 'main/sop_tab.html', locals())


@login_required
@apply_perms
def show_sop_tab(request, obj_id,**kwargs):
    user = request.user
    title = "Show SOP"
    obj = get_object_or_404(SOPTab, id=obj_id)
    missingLatestSOP = False

    orgs = SOPTab_Orgs.objects.filter(soptab=obj)
    sop_attachments = SOPTabAttachment.objects.filter(soptab=obj)
    sop_review_distributions = SOPTabReviewDistribution.objects.filter(soptab=obj)
    sop_approval_history = SOPTab_approval_history.objects.filter(soptab=obj)
    sop_version_history = SOPTab.objects.filter(sop_base_id=obj.sop_base_id).order_by('-sop_number')
    # Split out data from each log string so we can show it nicely in web page.
    parsed_logs = []
    if sop_review_distributions:
        for log in sop_review_distributions:
            logstr = log.the_name
            parsed_logs.append(logstr.split(CORRESPONDENCE_LOG_SPLITTER))

    if obj.sop_status.the_name == "Active":
        # check if there is an SOP attached
        has_sop = False
        for att in sop_attachments:
            if att.is_latest_sop == 'Y':
                has_sop = True
                break
        if not has_sop:
            if sop_attachments:
                message = "Active SOP does not have an attachment marked as the latest SOP. Toggle N to Y to indicate a file is the latest SOP."
            else:
                message = "Active SOP does not have any attachments. Upload the latest SOP and toggle N to Y to indicate it is the latest SOP."
            missingLatestSOP = True


    # Fill email subject line form field with default value.
    if obj.full_title:
        email_subject = "[SOP " + str(obj.sop_number) + "] " + obj.full_title
    else:
        email_subject = "SOP " + str(obj.sop_number)

    if request.method == "POST":

        if request.POST.get("send_the_emails"):

            from_email = settings.DEFAULT_QATRACK_EMAIL

            # Usually the user is also the contact or QA Manager, so don't add email twice.
            if user.email==obj.sop_contact.email or user.email==obj.approving_manager.email:
                to_emails = [obj.sop_contact.email, obj.approving_manager.email]
            else:
                to_emails = [user.email, obj.sop_contact.email, obj.approving_manager.email]

            if obj.sop_review_email_list is not None and len(obj.sop_review_email_list) > 0:
                for nonOrd in obj.sop_review_email_list.split():
                    nonOrd = nonOrd.replace(';', '')
                    nonOrd = nonOrd.replace(',', '')
                    to_emails.append(nonOrd)

            for ord in obj.sop_review_distribution_list.all():
                to_emails.append(ord.email)

            # to_emails = [user.email]   # testing only

            all_emails = ""
            for each_mail in to_emails:
                all_emails += "; " + each_mail

            email_notes = request.POST.get("email_notes", "")
            # Subject is now editable field.
            sop_number = obj.sop_number if obj.sop_number is not None else ""
            full_title = obj.full_title if obj.full_title is not None else "Untitled"
            sop_status = obj.sop_status.the_name if obj.sop_status is not None and obj.sop_status.the_name is not None else ""
            email_subject = request.POST.get("email_subject", "")
            email_body = "SOP Number: " + sop_number + "\r\n"

            # Include alternate and previous IDs, if any.
            if obj.alt_id:
                email_body = email_body + "Alternate ID: " + obj.alt_id + "\r\n"
            if obj.previous_id:
                email_body = email_body + "Previous ID: " + obj.previous_id + "\r\n"

            email_body = email_body + "SOP Title: " + full_title + "\r\nStatus: " + sop_status + "\r\n\r\n"
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
            for att in sop_attachments:
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
            sop_review_distribution = SOPTabReviewDistribution.objects.create(soptab=obj,
                                                      the_name=the_time.strftime("%Y-%m-%d %I:%M %p EST") +
                                                               CORRESPONDENCE_LOG_SPLITTER + all_emails[2:] +
                                                               CORRESPONDENCE_LOG_SPLITTER + email_subject +
                                                               CORRESPONDENCE_LOG_SPLITTER + att_listing +
                                                               CORRESPONDENCE_LOG_SPLITTER + email_body_log)

            url = '/sop_tab/show/%s/#correspondence' % str(obj.id)
            return HttpResponseRedirect(url)


    return render(request, 'show/show_sop_tab_item.html', locals())

@login_required
@apply_perms
def file_upload_soptab(request, obj_id,**kwargs):
    user = request.user
    profile = user.userprofile
    soptab = SOPTab.objects.get(id=obj_id)

#    if user.is_staff or profile.can_edit == "Y":
    error_message = "You can add files"
#    else:
#        error_message = "You are not authorized to add files."
#        back_link = "/sop_tab/show/"
#        return render(request, 'error.html', locals())

    for new_file in request.FILES.getlist('upl'):
        # Create a new entry in our database
        soptab_attachment, created = SOPTabAttachment.objects.get_or_create(soptab=soptab, attachment=new_file,
                                                                            the_name=new_file.name, user=user,
                                                                            the_size=new_file.size)

    url = '/sop_tab/show/%s/#attachments' % str(soptab.id)
    return HttpResponseRedirect(url)


# Archive the currently viewed SOP.
# Just set status to archived and redisplay the show screen.
@login_required
@apply_perms
def archive_sop_tab_item(request, obj_id, **kwargs):
    # Check if the SOP already has archived status.
    message = "This SOP has already been archived."

    user = request.user
    profile = user.userprofile

    obj = SOPTab.objects.get(id=obj_id)
    archived_obj = SOPTab_Status.objects.filter(the_name='Archived').first()

    if obj.sop_status != archived_obj:  # archived
        message = "SOP archived."

        obj.sop_status = archived_obj

        obj.save()

        # add to review history
        sop_review_distribution = SOPTab_approval_history.objects.create(soptab=obj,
                                                                         user=user,
                                                                         date_reviewed=obj.date_reviewed,
                                                                         sop_contact=obj.sop_contact,
                                                                         approving_manager=obj.approving_manager,
                                                                         sop_status=obj.sop_status,
                                                                         comments='SOP archived')


    orgs = SOPTab_Orgs.objects.filter(soptab=obj)
    sop_attachments = SOPTabAttachment.objects.filter(soptab=obj)
    sop_review_distributions = SOPTabReviewDistribution.objects.filter(soptab=obj)
    sop_approval_history = SOPTab_approval_history.objects.filter(soptab=obj)
    sop_version_history = SOPTab.objects.filter(sop_base_id=obj.sop_base_id).order_by('-sop_number').order_by('-sop_number')

    # Fill email subject line form field with default value.
    if obj.full_title:
        email_subject = "[SOP " + str(obj.sop_number) + "] " + obj.full_title
    else:
        email_subject = "SOP " + str(obj.sop_number)

    title = "Show SOP"

    return render(request, 'show/show_sop_tab_item.html', locals())


# Archive the currently viewed SOP and create a new SOP by copying the basic data
# and incrementing the version number.
# Display the new version in the show screen.
@login_required
@apply_perms
def create_new_sop_version(request, obj_id, **kwargs):
    # make sure user is on the latest version before creating a new one
    message = "New Version Not Created. A new version can only be created from the latest version."

    user = request.user
    profile = user.userprofile

    # create new and copy some fields
    obj = SOPTab.objects.get(id=obj_id)

    # get the latest version number to compare
    latest_version_num = SOPTab.objects.filter(sop_base_id=obj.sop_base_id).latest().sop_version

    # return HttpResponse(latest_version_num)   # test only

    if obj.sop_version == latest_version_num:
        message = "New Version Created. Don't forget to attach SOP and mark it as the latest SOP."

        new_sop = SOPTab()

        new_sop.previous_id = obj.previous_id
        new_sop.alt_id = obj.alt_id

        new_sop.full_title = obj.full_title
        new_sop.keywords = obj.keywords
        new_sop.sop_type = obj.sop_type
        new_sop.mural_type = obj.mural_type
        new_sop.sop_contact = obj.sop_contact
        new_sop.approving_manager = obj.approving_manager
        new_sop.approving_line_manager = obj.approving_line_manager

        new_sop.sop_review_email_list = obj.sop_review_email_list

        new_sop.office = obj.office
        new_sop.lab = obj.lab
        new_sop.division = obj.division
        new_sop.branch = obj.branch
        new_sop.user = obj.user
        new_sop.discipline = obj.discipline
        new_sop.subdiscipline = obj.subdiscipline

        # Create SOP number by incrementing version.
        new_sop.sop_base_number = obj.sop_base_number
        new_sop.sop_base_id = obj.sop_base_id
        new_sop.sop_version = obj.sop_version + 1
        new_sop.sop_number = new_sop.sop_base_number + "-" + str(new_sop.sop_version)

        new_sop.sop_status = SOPTab_Status.objects.filter(the_name='Active').first()

        new_sop.save()

        # projects, programs, related sops, participating orgs, email list
        for each_proj in obj.projects.all():
            new_sop.projects.add(each_proj)

        for each_program in obj.programs.all():
            new_sop.programs.add(each_program)

        for each_sop in obj.related_sops.all():
            new_sop.related_sops.add(each_sop)

        for each_participating_org in obj.participating_orgs.all():
            new_sop.participating_orgs.add(each_participating_org)

        for each_ORDEmail in obj.sop_review_distribution_list.all():
            new_sop.sop_review_distribution_list.add(each_ORDEmail)

        # related ord orgs
        related_orgs = SOPTab_Orgs.objects.filter(soptab=obj)
        for each_org in related_orgs:
            new_related_org = SOPTab_Orgs()
            new_related_org.soptab = new_sop
            new_related_org.office = each_org.office
            new_related_org.lab = each_org.lab
            new_related_org.division = each_org.division
            new_related_org.branch = each_org.branch
            new_related_org.save()

        # Set the previous version to archived.
        obj.sop_status = SOPTab_Status.objects.filter(the_name='Archived').first()

        # mark sop as not current
        obj.is_current = 'N'

        obj.save()

        # url = '/sop_tab/show/%s/' % str(new_sop.id)
        # return HttpResponseRedirect(url)

        # add to review history
        sop_review_distribution = SOPTab_approval_history.objects.create(soptab=obj,
                                                                         user=user,
                                                                         date_reviewed=obj.date_reviewed,
                                                                         sop_contact=obj.sop_contact,
                                                                         approving_manager=obj.approving_manager,
                                                                         sop_status=obj.sop_status,
                                                                         comments='This SOP version archived as new version created')

        obj = new_sop

        # add to review history
        sop_review_distribution = SOPTab_approval_history.objects.create(soptab=new_sop,
                                                                         user=user,
                                                                         date_reviewed=new_sop.date_reviewed,
                                                                         sop_contact=new_sop.sop_contact,
                                                                         approving_manager=new_sop.approving_manager,
                                                                         sop_status=new_sop.sop_status,
                                                                         comments='This SOP version created')



    orgs = SOPTab_Orgs.objects.filter(soptab=obj)
    sop_attachments = SOPTabAttachment.objects.filter(soptab=obj)
    sop_review_distributions = SOPTabReviewDistribution.objects.filter(soptab=obj)
    sop_approval_history = SOPTab_approval_history.objects.filter(soptab=obj)
    sop_version_history = SOPTab.objects.filter(sop_base_id=obj.sop_base_id).order_by('-sop_number')



    # Fill email subject line form field with default value.
    if obj.full_title:
        email_subject = "[SOP " + str(obj.sop_number) + "] " + obj.full_title
    else:
        email_subject = "SOP " + str(obj.sop_number)

    title = "Show SOP"

    return render(request, 'show/show_sop_tab_item.html', locals())


class CreateOrgLink_SOP(FormView):
    template = "main/link_organization_sop.html"

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id, **kwargs):
        """
        Start a new project
        """
        # return HttpResponse("G")   test only

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
    def post(self, request, obj_id, **kwargs):
        """
        Create the Org Link (entry into linking table)
        """

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)

        if (office_id):

            org_link = SOPTab_Orgs()
            soptab = get_object_or_404(SOPTab, id=obj_id)
            org_link.soptab = soptab

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

            url = '/sop_tab/show/%s/#relatedorgs' % str(obj_id)
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
def delete_sop_org(request, obj_id, **kwargs):
    user = request.user
    sop_org = get_object_or_404(SOPTab_Orgs, id=obj_id)

#    if user.is_staff:
    sop_org.delete()

    url = '/sop_tab/show/%s/#relatedorgs' % str(sop_org.soptab_id)
    return HttpResponseRedirect(url)


@login_required
@apply_perms
def switch_file_email_flag_sop(request, obj_id, **kwargs):
    user = request.user
    sop_attachment = get_object_or_404(SOPTabAttachment, id=obj_id)

    if sop_attachment.include_in_email != "Y":
        sop_attachment.include_in_email = "Y"
    else:
        sop_attachment.include_in_email = "N"

    sop_attachment.save()

    url = '/sop_tab/show/%s/#attachments' % str(sop_attachment.soptab_id)
    return HttpResponseRedirect(url)


@login_required
@apply_perms
def switch_is_review_file_flag_sop(request, obj_id, **kwargs):
    user = request.user
    sop_attachment = get_object_or_404(SOPTabAttachment, id=obj_id)

    if sop_attachment.is_latest_sop == "N":
        if sop_attachment.is_review_file != "Y":
            sop_attachment.is_review_file = "Y"
        else:
            sop_attachment.is_review_file = "N"

    sop_attachment.save()

    url = '/sop_tab/show/%s/#attachments' % str(sop_attachment.soptab_id)
    return HttpResponseRedirect(url)


@login_required
@apply_perms
def switch_is_latest_SOP_sop(request, obj_id, **kwargs):
    user = request.user
    sop_attachment = get_object_or_404(SOPTabAttachment, id=obj_id)

    if sop_attachment.is_latest_sop != "Y":
        # go thru all the sop versions and set any 'Y' to 'N'
        sop_version_history = SOPTab.objects.filter(sop_base_id=sop_attachment.soptab.sop_base_id).order_by('-sop_number')
        for each_sop in sop_version_history:
            # get the attacment records
            sop_version_attachments = SOPTabAttachment.objects.filter(soptab=each_sop)
            for each_attachment in sop_version_attachments:
                if each_attachment.is_latest_sop == 'Y':
                    each_attachment.is_latest_sop = 'N'
                    each_attachment.is_review_file = 'N'
                    each_attachment.save()

        # set current selection to 'Y'
        sop_attachment.is_latest_sop = "Y"
        sop_attachment.is_review_file = "Y"

    else:
        sop_attachment.is_latest_sop = "N"
        sop_attachment.is_review_file = "N"

    sop_attachment.save()

    url = '/sop_tab/show/%s/#attachments' % str(sop_attachment.soptab_id)
    return HttpResponseRedirect(url)


@login_required
@apply_perms
def delete_soptab_attachment(request, obj_id, **kwargs):
    user = request.user
    sop_attachment = get_object_or_404(SOPTabAttachment, id=obj_id)
    sop = sop_attachment.soptab
    sop_tab_id = sop.id

    profile = user.userprofile
    obj = get_object_or_404(SOPTab, id=sop_tab_id)

    sop_attachments = SOPTabAttachment.objects.filter(soptab=obj)

    try:
#        if sop_attachment.user == user or profile.user_type == "SUPER":
        sop_attachment.delete()
        url = '/sop_tab/show/%s/#attachments' % str(sop_attachment.soptab_id)
        return HttpResponseRedirect(url)
#        else:
#            error = "You are not authorized to delete this attachment."
    except:
        error = "Failed to delete attachment. Please try again."

    return render(request, 'show/show_sop_tab_item.html', locals())


@login_required
@apply_perms
def search_sop_tab(request, **kwargs):
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

    # get discipline data
    discipline_required = True
    subdiscipline_required = False
    discipline_list = sopq.get_discipline_list(as_json=True, include_inactive=True)
    subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    # Need these to populate the dropdowns
    # Include only active for status because there is an inactive "No Entry" value not in use that we don't want to appear.
    sop_statuses = SOPTab_Status.objects.filter(is_active="Y").order_by('sort_number')
    sop_types = SOPTab_Type.objects.all().order_by('the_name')
    # Include only active for muraltype because there is an inactive "No Entry" value not in use that we don't want to appear.
    mural_types = SOPTab_MuralType.objects.filter(is_active="Y")
    external_orgs = ParticipatingOrganization.objects.all()
    programs = Program.objects.all().order_by('the_name')

    return render(request, 'main/search_sop_tab.html', locals())


@login_required
@apply_perms
def result_search_sop_tab(request, **kwargs):
    user = request.user

    query = Q()
    query_show = ''
    the_count = 0

    title = "Search For SOPs - With Results Shown"

    if request is None:
        return SOPTab.objects.get(id=1)

    # Lead Organization
    lead_office_id = request.GET.get("office", None)
    lead_lab_id = request.GET.get("lab", None)
    lead_division_id = request.GET.get("division", None)
    lead_branch_id = request.GET.get("branch", None)

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


    # Discipline and Subdiscipline
    discipline_id = request.GET.get("discipline", None)
    subdiscipline_id = request.GET.get("subdiscipline", None)

    if discipline_id is not None and discipline_id != '':
        discipline = Discipline.objects.get(id=discipline_id)
        query = query & (Q(discipline_id=discipline_id))
        query_show = query_show + "Discipline = " + str(discipline) + " "

    if subdiscipline_id is not None and subdiscipline_id != '':
        subdiscipline = SubDiscipline.objects.get(id=subdiscipline_id)
        query = query & (Q(subdiscipline_id=subdiscipline_id))
        query_show = query_show + "Subdiscipline = " + str(subdiscipline) + " "


    if 'sop_number' in request.GET:
        sop_number = request.GET['sop_number']
        sop_number = sop_number.strip()  # Trim white space
        if sop_number:
            query = query & (Q(sop_number__icontains=sop_number))
            query_show = query_show + "SOP Number = " + str(sop_number) + " "

    if 'full_title' in request.GET:
        full_title = request.GET['full_title']
        if full_title:
            query = query & (Q(full_title__icontains=full_title))
            query_show = query_show + "Full Title = " + str(full_title) + " "

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

    # SOP Status
    item_01 = ''
    sub_query_01 = Q()
    sub_query_show_01 = ''
    if 'sop_status' in request.GET:
        sop_stats = request.GET.getlist('sop_status')
        if sop_stats:
            for item_01 in sop_stats:
                a_status = SOPTab_Status.objects.get(id=item_01)
                sub_query_01 = sub_query_01 | Q(sop_status_id=item_01)
                sub_query_show_01 = sub_query_show_01 + a_status.the_name + ", "

            query = sub_query_01 & query
            query_show = query_show + "SOP Status(es) => " + sub_query_show_01

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query = query & (Q(keywords__icontains=keywords))
            query_show = query_show + "Keyword = " + str(keywords) + " "

    # SOP Type
    item_02 = ''
    sub_query_02 = Q()
    sub_query_show_02 = ''
    if 'sop_type' in request.GET:
        sop_type = request.GET.getlist('sop_type')
        if sop_type:
            for item_02 in sop_type:
                a_type = SOPTab_Type.objects.get(id=item_02)
                sub_query_02 = sub_query_02 | Q(sop_type_id=item_02)
                sub_query_show_02 = sub_query_show_02 + a_type.the_name + ", "

            query = sub_query_02 & query
            query_show = query_show + "SOP Type(s) => " + sub_query_show_02

    # Intramural or Extramural
    item_03 = ''
    sub_query_03 = Q()
    sub_query_show_03 = ''
    if 'mural' in request.GET:
        murals = request.GET.getlist('mural')
        if murals:
            for item_03 in murals:
                a_mural = SOPTab_MuralType.objects.get(id=item_03)
                sub_query_03 = sub_query_03 | Q(mural_type_id=item_03)
                sub_query_show_03 = sub_query_show_03 + a_mural.the_name + ", "

            query = sub_query_03 & query
            query_show = query_show + "Intra/Extramural => " + sub_query_show_03

    if 'contact_last' in request.GET:
        contact_last = request.GET['contact_last']
        if contact_last:
            query = query & (Q(sop_contact__last_name__istartswith=contact_last))
            query_show = query_show + "SOP Contact Last Name = " + str(contact_last) + " "

    if 'contact_first' in request.GET:
        contact_first = request.GET['contact_first']
        if contact_first:
            query = query & (Q(sop_contact__first_name__istartswith=contact_first))
            query_show = query_show + "SOP Contact First Name = " + str(contact_first) + " "

    if 'approving_manager_last' in request.GET:
        approving_manager_last = request.GET['approving_manager_last']
        if approving_manager_last:
            query = query & (Q(approving_manager__last_name__istartswith=approving_manager_last))
            query_show = query_show + "Approving QA Manager Last Name = " + str(approving_manager_last) + " "

    if 'approving_manager_first' in request.GET:
        approving_manager_first = request.GET['approving_manager_first']
        if approving_manager_first:
            query = query & (Q(approving_manager__first_name__istartswith=approving_manager_first))
            query_show = query_show + "Approving QA Manager First Name = " + str(approving_manager_first) + " "

    if 'approving_line_manager_last' in request.GET:
        approving_line_manager_last = request.GET['approving_line_manager_last']
        if approving_line_manager_last:
            query = query & (Q(approving_line_manager__last_name__istartswith=approving_line_manager_last))
            query_show = query_show + "Approving Line Manager Last Name = " + str(approving_line_manager_last) + " "

    if 'approving_line_manager_first' in request.GET:
        approving_line_manager_first = request.GET['approving_line_manager_first']
        if approving_line_manager_first:
            query = query & (Q(approving_line_manager__first_name__istartswith=approving_line_manager_first))
            query_show = query_show + "Approving Line Manager First Name = " + str(approving_line_manager_first) + " "

    # Date Approved
    if 'no_date_approved' in request.GET:
        query = query & (Q(date_approved=None))
        query_show = query_show + "No Date SOP Approved "
    else:
        if 'date_approved_f' in request.GET:
            date_approved_f = request.GET['date_approved_f']
            if date_approved_f:
                query = query & (Q(date_approved__gte=date_approved_f))
                query_show = query_show + "Date SOP Approved From Date = " + str(date_approved_f) + " "
        if 'date_approved_t' in request.GET:
            date_approved_t = request.GET['date_approved_t']
            if date_approved_t:
                query = query & (Q(date_approved__lte=date_approved_t))
                query_show = query_show + "Date SOP Approved To Date = " + str(date_approved_t) + " "

    # Date Effective
    if 'no_date_effective' in request.GET:
        query = query & (Q(date_effective=None))
        query_show = query_show + "No Date SOP Effective "
    else:
        if 'date_effective_f' in request.GET:
            date_effective_f = request.GET['date_effective_f']
            if date_effective_f:
                query = query & (Q(date_effective__gte=date_effective_f))
                query_show = query_show + "Date SOP Effective From Date = " + str(date_effective_f) + " "
        if 'date_effective_t' in request.GET:
            date_effective_t = request.GET['date_effective_t']
            if date_effective_t:
                query = query & (Q(date_effective__lte=date_effective_t))
                query_show = query_show + "Date SOP Effective To Date = " + str(date_effective_t) + " "

    # Date of Last Review
    if 'no_date_reviewed' in request.GET:
        query = query & (Q(date_reviewed=None))
        query_show = query_show + "No Date SOP Reviewed "
    else:
        if 'date_reviewed_f' in request.GET:
            date_reviewed_f = request.GET['date_reviewed_f']
            if date_reviewed_f:
                query = query & (Q(date_reviewed__gte=date_reviewed_f))
                query_show = query_show + "Date SOP Reviewed From Date = " + str(date_reviewed_f) + " "
        if 'date_reviewed_t' in request.GET:
            date_reviewed_t = request.GET['date_reviewed_t']
            if date_reviewed_t:
                query = query & (Q(date_reviewed__lte=date_reviewed_t))
                query_show = query_show + "Date SOP Reviewed To Date = " + str(date_reviewed_t) + " "

    # SOPs can be associated with multiple projects.
    # Search for SOPs linked to this project ID.
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

    # Related SOPs
    if 'related_sop' in request.GET:
        related_sop = request.GET['related_sop']
        if related_sop:
            query = query & (Q(related_sops__sop_number__icontains=related_sop))
            query_show = query_show + "Related SOP Number contains " + str(related_sop) + " "

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
    office_id = request.GET.get("office2", None)
    lab_id = request.GET.get("lab2", None)
    division_id = request.GET.get("division2", None)
    branch_id = request.GET.get("branch2", None)

    if office_id is not None and office_id != '':
        office = Office.objects.get(id=office_id)
        query = query & (Q(soptab_orgs__office_id=office_id))
        prev_query_show = query_show
        query_show = prev_query_show + "Related ORD Organization = " + str(office) + " "

        if lab_id is not None and lab_id != '':
            lab = Lab.objects.get(id=lab_id)
            query = query & (Q(soptab_orgs__lab_id=lab_id))
            query_show = prev_query_show + "Related ORD Organization = " + str(lab) + " "

            if division_id is not None and division_id != '':
                division = Division.objects.get(id=division_id)
                query = query & (Q(soptab_orgs__division_id=division_id))
                query_show = prev_query_show + "Related ORD Organization = " + str(division) + " "

                if branch_id is not None and branch_id != '':
                    branch = Branch.objects.get(id=branch_id)
                    query = query & (Q(soptab_orgs__branch_id=branch_id))
                    query_show = prev_query_show + "Related ORD Organization = " + str(branch) + " "

    # Comments
    if 'comments' in request.GET:
        comments = request.GET['comments']
        if comments:
            query = query & (Q(comments__icontains=comments))
            query_show = query_show + "Comments contain \"" + str(comments) + "\" "


    objs = SOPTab.objects.filter(query).distinct()
    the_count = len(objs)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    if 'excel' in request.GET and the_count>0:
        excel = request.GET['excel']
        if excel == "Y":
            sops = objs
            the_count = SOPTab.objects.filter(query).count()

            response = HttpResponse(content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=sops_searched.xls'
            wb = xlwt.Workbook()
            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            sheet = wb.add_sheet('SOPs')


            sheet.write(0, 0, 'SOP Number')
            sheet.write(0, 1, 'Previous ID')
            sheet.write(0, 2, 'Alternate ID')
            sheet.write(0, 3, 'Status')
            sheet.write(0, 4, 'Full Title')
            sheet.write(0, 5, 'Keywords')

            sheet.write(0, 6, 'Comments')
            sheet.write(0, 7, 'SOP Type')
            sheet.write(0, 8, 'Intramural or Extramural')

            sheet.write(0, 9, 'Lead Organization Office')
            sheet.write(0, 10, 'Lead Organization Center/Office')
            sheet.write(0, 11, 'Lead Organization Division')
            sheet.write(0, 12, 'Lead Organization Branch')

            sheet.write(0, 13, 'Discipline')
            sheet.write(0, 14, 'Subdiscipline')

            sheet.write(0, 15, 'SOP Contact First')
            sheet.write(0, 16, 'SOP Contact Last')
            sheet.write(0, 17, 'Approving QA Manager First')
            sheet.write(0, 18, 'Approving QA Manager Last')
            sheet.write(0, 19, 'Approving Line Manager First')
            sheet.write(0, 20, 'Approving Line Manager Last')

            sheet.write(0, 21, 'Date Approved')
            sheet.write(0, 22, 'Date Effective')
            sheet.write(0, 23, 'Date of Last Review')

            sheet.write(0, 24, 'Project IDs')
            sheet.write(0, 25, 'Programs')
            sheet.write(0, 26, 'Related SOPs')
            sheet.write(0, 27, 'Related EPA Non-ORD Organizations')
            sheet.write(0, 28, 'Related ORD Organizations')

            sheet.write(0, 29, 'Follow-up Email List (ORD)')
            sheet.write(0, 30, 'Follow-up Email List (non-ORD)')

            i = 1
            for obj in sops:

                sheet.write(i, 0, obj.sop_number)
                sheet.write(i, 1, obj.previous_id)
                sheet.write(i, 2, obj.alt_id)

                if obj.sop_status is not None:
                    sheet.write(i, 3, obj.sop_status.the_name)
                else:
                    sheet.write(i, 3, '')

                sheet.write(i, 4, obj.full_title)
                sheet.write(i, 5, obj.keywords)
                sheet.write(i, 6, obj.comments)

                if obj.sop_type is not None:
                    sheet.write(i, 7, obj.sop_type.the_name)
                else:
                    sheet.write(i, 7, '')

                if obj.mural_type is not None:
                    sheet.write(i, 8, obj.mural_type.the_name)
                else:
                    sheet.write(i, 8, '')

                if obj.office is not None:
                    sheet.write(i, 9, obj.office.abbreviation)
                else:
                    sheet.write(i, 9, '')

                if obj.lab is not None:
                    sheet.write(i, 10, obj.lab.abbreviation)
                else:
                    sheet.write(i, 10, '')

                if obj.division is not None:
                    sheet.write(i, 11, obj.division.abbreviation)
                else:
                    sheet.write(i, 11, '')

                if obj.branch is not None:
                    sheet.write(i, 12, obj.branch.abbreviation)
                else:
                    sheet.write(i, 12, '')

                if obj.discipline is not None:
                    sheet.write(i, 13, obj.discipline.discipline)
                else:
                    sheet.write(i, 13, '')

                if obj.subdiscipline is not None:
                    sheet.write(i, 14, obj.subdiscipline.subdiscipline)
                else:
                    sheet.write(i, 14, '')

                if obj.sop_contact is not None:
                    sheet.write(i, 15, obj.sop_contact.first_name)
                    sheet.write(i, 16, obj.sop_contact.last_name)
                else:
                    sheet.write(i, 15, '')
                    sheet.write(i, 16, '')

                if obj.approving_manager is not None:
                    sheet.write(i, 17, obj.approving_manager.first_name)
                    sheet.write(i, 18, obj.approving_manager.last_name)
                else:
                    sheet.write(i, 17, '')
                    sheet.write(i, 18, '')

                if obj.approving_line_manager is not None:
                    sheet.write(i, 19, obj.approving_line_manager.first_name)
                    sheet.write(i, 20, obj.approving_line_manager.last_name)
                else:
                    sheet.write(i, 19, '')
                    sheet.write(i, 20, '')

                sheet.write(i, 21, obj.date_approved, style=styles["date"])
                sheet.write(i, 22, obj.date_effective, style=styles["date"])
                sheet.write(i, 23, obj.date_reviewed, style=styles["date"])

                # Combine any project ids into one string
                if obj.projects is not None:
                    projects = obj.projects.all()
                    project_ids = ''
                    for proj in projects:
                        if project_ids=='':
                            project_ids = proj.qa_id
                        else:
                            project_ids = project_ids + ';' + proj.qa_id
                    sheet.write(i, 24, project_ids)
                else:
                    sheet.write(i, 24, '')

                # Combine any programs into one string
                if obj.programs is not None:
                    programs = obj.programs.all()
                    programs_str = ''
                    for prog in programs:
                        if programs_str == '':
                            programs_str = prog.the_name
                        else:
                            programs_str = programs_str + ';' + prog.the_name
                    sheet.write(i, 25, programs_str)
                else:
                    sheet.write(i, 25, '')

                # Combine any related SOP numbers into one string
                if obj.related_sops is not None:
                    related_sops = obj.related_sops.all()
                    sop_nums = ''
                    for sop in related_sops:
                        if sop_nums == '':
                            sop_nums = sop.sop_number
                        else:
                            sop_nums = sop_nums + ';' + sop.sop_number
                    sheet.write(i, 26, sop_nums)
                else:
                    sheet.write(i, 26, '')

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
                    sheet.write(i, 27, partic_orgs_str)
                else:
                    sheet.write(i, 27, '')

                # ORD Organizations
                orgs = SOPTab_Orgs.objects.filter(soptab=obj)
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

                sheet.write(i, 28, related_orgs)

                # ORD Emails
                ord_people = ''
                for person in obj.sop_review_distribution_list.all():
                    if ord_people == '':
                        ord_people = person.email
                    else:
                        ord_people = ord_people + ';' + person.email

                sheet.write(i, 29, ord_people)

                # non-ORD Emails
                sheet.write(i, 30, obj.sop_review_email_list)

                i += 1

            sheet1 = wb.add_sheet('Query')
            sheet1.write(1, 0, query_show)

            wb.save(response)
            return response


    return render(request, 'main/search_sop_tab_result.html', locals())


@login_required
@apply_perms
def search_sop_sepcontact(request, **kwargs):
    user = request.user
    title = "Search SOPs"

    # get the organization data
    office_list = oq.get_unrestricted_office_list(user, as_json=True)
    lab_list = oq.get_unrestricted_lab_list(user, None, as_json=True)
    division_list = oq.get_unrestricted_division_list(user, None, None, as_json=True)
    branch_list = oq.get_unrestricted_branch_list(user, None, None, None, as_json=True)

    # NOTE: we do not set the selected_office to the user's office because
    # audits may not be linked to any audited ORD organization.
    # Hence we do not want a default value in the audited ORD organization fields.
    # However, it's ok to set office for Lead Organization
    selected_office = user.userprofile.office
    selected_lab = user.userprofile.lab
    selected_division = user.userprofile.division

    label_class = "col-sm-4"
    input_container_class = "col-sm-8"

    # Need these to populate the dropdowns
    # Include only active for status because there is an inactive "No Entry" value not in use that we don't want to appear.
    sop_statuses = SOPTab_Status.objects.filter(is_active="Y").order_by('sort_number')

    return render(request, 'main/search_sop_sepcontact.html', locals())

@login_required
@apply_perms
def result_search_sop_sepcontact(request, **kwargs):
    user = request.user

    query = Q()
    query_show = ''
    the_count = 0

    title = "Search SOPs with Separated SOP Contact - With Results Shown"

    if request is None:
        return SOPTab.objects.get(id=1)

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

    # SOP Status
    item_06 = ''
    sub_query_06 = Q()
    sub_query_show_06 = ''
    if 'sop_status' in request.GET:
        sop_status = request.GET.getlist('sop_status')

        if sop_status:
            for item_06 in sop_status:
                b_status = SOPTab_Status.objects.get(id=item_06)
                sub_query_06 = sub_query_06 | Q(sop_status_id=item_06)
                sub_query_show_06 = sub_query_show_06 + b_status.the_name + ", "

            query = sub_query_06 & query
            query_show = query_show + "SOP Status(es) => " + sub_query_show_06

    objs = (
        SOPTab.objects
            .filter(query)
            .distinct()
    )

    the_count = len(objs)

    # Clean up dangling comma.
    last_two = query_show[len(query_show) - 2:]
    if last_two == ', ':
        query_show = query_show[:-2]

    wanted_items = set()

    for sop in objs:

        has_issue = False

        # Check if SOP contact has separated.
        if sop.sop_contact is not None:
            if sop.sop_contact.userprofile.date_epa_separation is not None:
                today = timezone.now().date()
                if sop.sop_contact.userprofile.date_epa_separation <= today:
                    has_issue = True

        if has_issue == True:
            wanted_items.add(sop.pk)

    objs = objs.filter(pk__in=wanted_items)
    the_count = len(objs)


    ############
    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count > 0:
        excel = request.GET['excel']
        if excel == "Y":
            # Export to Excel
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=SOPsSeparatedContact.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            worksheet = workbook.add_worksheet('SOPs with Separated Contact')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "SOPs with Separated SOP Contact", section_format)

            row += 1
            today = timezone.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2
            worksheet.write(row, 0, "Office", label_format)
            worksheet.write(row, 1, "Center", label_format)
            worksheet.write(row, 2, "Division", label_format)
            worksheet.write(row, 3, "Branch", label_format)
            worksheet.write(row, 4, "SOP Number", label_format)
            worksheet.write(row, 5, "Previous ID", label_format)
            worksheet.write(row, 6, "Alternate ID", label_format)
            worksheet.write(row, 7, "Full Title", label_format)
            worksheet.write(row, 8, "Status", label_format)
            worksheet.write(row, 9, "Intramural or Extramural", label_format)
            worksheet.write(row, 10, "SOP Contact", label_format)
            worksheet.write(row, 11, "SOP Contact Separation Date", label_format)
            worksheet.write(row, 12, "Approving QA Manager", label_format)
            worksheet.write(row, 13, "Approving Line Manager", label_format)
            worksheet.write(row, 14, "Date Approved", label_format)
            worksheet.write(row, 15, "Date Effective", label_format)
            worksheet.write(row, 16, "Date Reviewed", label_format)

            for sop in objs:
                row += 1
                worksheet.write(row, 0, sop.office.abbreviation)
                if sop.lab:
                    worksheet.write(row, 1, sop.lab.abbreviation)
                else:
                    worksheet.write(row, 1, "")
                if sop.division:
                    worksheet.write(row, 2, sop.division.abbreviation)
                else:
                    worksheet.write(row, 2, "")
                if sop.branch:
                    worksheet.write(row, 3, sop.branch.abbreviation)
                else:
                    worksheet.write(row, 3, "")
                worksheet.write(row, 4, sop.sop_number)
                worksheet.write(row, 5, sop.previous_id)
                worksheet.write(row, 6, sop.alt_id)
                worksheet.write(row, 7, sop.full_title)
                worksheet.write(row, 8, sop.sop_status.the_name)

                if sop.mural_type is not None:
                    worksheet.write(row, 9, sop.mural_type.the_name)
                else:
                    worksheet.write(row, 9, '')

                worksheet.write(row, 10, sop.sop_contact.first_name + " " + sop.sop_contact.last_name)
                if sop.sop_contact.userprofile.date_epa_separation:
                    worksheet.write(row, 11, str(sop.sop_contact.userprofile.date_epa_separation))
                else:
                    worksheet.write(row, 11, "")

                if sop.approving_manager is not None:
                    worksheet.write(row, 12, sop.approving_manager.first_name + " " + sop.approving_manager.last_name)
                else:
                    worksheet.write(row, 12, "")

                if sop.approving_line_manager is not None:
                    worksheet.write(row, 13, sop.approving_line_manager.first_name + " " + sop.approving_line_manager.last_name)
                else:
                    worksheet.write(row, 13, "")

                worksheet.write(row, 14, str(sop.date_approved))
                worksheet.write(row, 15, str(sop.date_effective))
                worksheet.write(row, 16, str(sop.date_reviewed))


            # wrap up - Add a sheet with the query
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, query_show)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response

    return render(request, 'main/search_sop_sepcontact_result.html', locals())


class SOPTabEditView(FormView):

    form_class = SOPTabFormAsync
    template = 'main/edit_sop_tab_item.html'


    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id, **kwargs):

        obj = get_object_or_404(SOPTab, id=obj_id)

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

        # get discipline data
        discipline_list = sopq.get_discipline_list(as_json=True)
        subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True)
        discipline_required = True
        subdiscipline_required = False

        selected_discipline = obj.discipline
        selected_subdiscipline = obj.subdiscipline

        sop_approval_history = SOPTab_approval_history.objects.filter(soptab=obj)

        # include inactive disciplines and subdisciplines if the selected one is inactive.
        if selected_discipline and selected_discipline.is_active=='N':
            discipline_list = sopq.get_discipline_list(as_json=True, include_inactive=True)
            subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)
        else:
            discipline_list = sopq.get_discipline_list(as_json=True)
            if selected_subdiscipline and selected_subdiscipline.is_active=='N':
                subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)
            else:
                subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True)

        return render(request, self.template, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, obj_id, **kwargs):

        user = request.user
        obj = get_object_or_404(SOPTab, id=obj_id)

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

        # get discipline data
        discipline_list = sopq.get_discipline_list(as_json=True, include_inactive=True)
        subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)
        discipline_required = True
        subdiscipline_required = False

        # Save the sop_version before it's wiped out so we can set it to this value again
        # as it's not included in the edit form.
        the_version = obj.sop_version

        form = self.form_class(data=request.POST, files=request.FILES, instance=obj)

        before_date_reviewed = obj.date_reviewed
        before_sop_contact = obj.sop_contact
        before_approving_manager = obj.approving_manager
        before_sop_status = obj.sop_status
        update_comments = request.POST.get("update_comment")

        if form.is_valid():

            soptab = form.save(commit=False)

            soptab.sop_version = the_version

            org_changed = False
            if selected_office != soptab.office:
                org_changed = True
            elif selected_lab != soptab.lab:
                org_changed = True
            elif selected_division != soptab.division:
                org_changed = True
            elif selected_branch != soptab.branch:
                org_changed = True

            if org_changed:
                # rebuild SOP Number
                base_id = soptab.sop_base_id
                base_sop_num = "H" if soptab.lab.designation_code is None else str(soptab.lab.designation_code)
                base_sop_num += "-" + str(soptab.division.abbreviation)
                if soptab.branch:
                    base_sop_num += "-" + str(soptab.branch.abbreviation)
                base_sop_num += "-SOP-" + str(base_id)

                soptab.sop_base_number = base_sop_num
                soptab.sop_base_id = base_id
                soptab.sop_number = base_sop_num + "-" + str(soptab.sop_version)

            soptab.save()
            form.save_m2m()

            log_hist = False
            if before_date_reviewed != soptab.date_reviewed:
                log_hist = True
            elif before_sop_contact != soptab.sop_contact:
                log_hist = True
            elif before_approving_manager != soptab.approving_manager:
                log_hist = True
            elif before_sop_status != soptab.sop_status:
                log_hist = True
            elif update_comments:
                log_hist = True

            if log_hist:
                # add to update history
                sop_approval_history = SOPTab_approval_history.objects.create(soptab=obj,
                                                                         user=user,
                                                                         date_reviewed=obj.date_reviewed,
                                                                         sop_contact=obj.sop_contact,
                                                                         approving_manager=obj.approving_manager,
                                                                         sop_status=obj.sop_status,
                                                                         comments=update_comments)

            url = '/sop_tab/show/%s/' % str(soptab.id)
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
            show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

            selected_discipline_id = request.POST.get("discipline", None)
            if selected_discipline_id:
                selected_discipline = get_object_or_404(Discipline, id=selected_discipline_id)
                selected_subdiscipline_id = request.POST.get("subdiscipline", None)
                if selected_subdiscipline_id:
                    selected_subdiscipline = get_object_or_404(SubDiscipline, id=selected_subdiscipline_id)

            # include inactive disciplines and subdisciplines if the selected one is inactive.
            if selected_discipline and selected_discipline.is_active == 'N':
                discipline_list = sopq.get_discipline_list(as_json=True, include_inactive=True)
                subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)
            else:
                discipline_list = sopq.get_discipline_list(as_json=True)
                if selected_subdiscipline and selected_subdiscipline.is_active == 'N':
                    subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True, include_inactive=True)
                else:
                    subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True)

            return render(request, self.template, locals())



# Create SOP
class SOPTabCreateView(FormView):

    form_class = SOPTabFormAsync
    template = 'main/create_sop_tab_item.html'

    def _valid_org_id(self, value):
        return (value is not None and value != '')

    @method_decorator(login_required)
    @apply_perms
    def get(self, request, obj_id, **kwargs):

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

        # get discipline data
        discipline_required = True
        subdiscipline_required = False
        discipline_list = sopq.get_discipline_list(as_json=True)
        subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True)

        # set office default
        selected_office = user.userprofile.office

        # Display the create form
        if not ((obj_id is None) or (obj_id == '0')):
            # Got here from Add SOP to Project menu choice.
            # Select the project as initial value of projects field.
            # Fill in the Lead Organization fields from the project organization.
            query = (Q(id__exact=obj_id))
            project_queryset = Project.objects.filter(query)
            selected_office = project_queryset[0].office
            selected_lab = project_queryset[0].lab
            selected_division = project_queryset[0].division
            selected_branch = project_queryset[0].branch

            #show_inactive = True

            form = self.form_class(initial={'projects': project_queryset})  # set default

        return render(request, self.template, locals())

    @method_decorator(login_required)
    @apply_perms
    def post(self, request, **kwargs):

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

        # get discipline data
        discipline_required = True
        subdiscipline_required = False
        discipline_list = sopq.get_discipline_list(as_json=True)
        subdiscipline_list = sopq.get_subdiscipline_list(None, as_json=True)

        office_id = request.POST.get("office", None)
        lab_id = request.POST.get("lab", None)
        division_id = request.POST.get("division", None)
        branch_id = request.POST.get("branch", None)
        show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

        discipline_id = request.POST.get("discipline", None)
        subdiscipline_id = request.POST.get("subdiscipline", None)

        if form.is_valid():
            soptab = form.save(commit=False)
            soptab.user = user

            soptab.save()
            form.save_m2m()

            # create SOP Number
            base_id = soptab.id
            lab_obj = get_object_or_404(Lab, id=lab_id)
            base_sop_num = "H" if lab_obj.designation_code is None else str(lab_obj.designation_code)
            division_obj = get_object_or_404(Division, id=division_id)
            base_sop_num += "-" + str(division_obj.abbreviation)
            if branch_id:
                branch_obj = get_object_or_404(Branch, id=branch_id)
                base_sop_num += "-" + str(branch_obj.abbreviation)
            base_sop_num += "-SOP-" + str(base_id)

            soptab.sop_base_number = base_sop_num
            soptab.sop_base_id = base_id

            # Default version is 0
            if soptab.sop_version is None:
                soptab.sop_version = 0

            soptab.sop_number = base_sop_num + "-" + str(soptab.sop_version)
            ###

            soptab.save()

            # add to update history
            sop_update_history = SOPTab_approval_history(
                soptab=soptab,
                user=user,
                date_reviewed=soptab.date_reviewed,
                sop_contact=soptab.sop_contact,
                approving_manager=soptab.approving_manager,
                sop_status=soptab.sop_status,
                comments='SOP created'
                )

            sop_update_history.save()
            url = '/sop_tab/show/%s/' % str(soptab.id)
            return HttpResponseRedirect(url)
        else:

            selected_office = Office.objects.get(id=office_id) if self._valid_org_id(office_id) else None
            selected_lab = Lab.objects.get(id=lab_id) if self._valid_org_id(lab_id) else None
            selected_division = Division.objects.get(id=division_id) if self._valid_org_id(division_id) else None
            selected_branch = Branch.objects.get(id=branch_id) if self._valid_org_id(branch_id) else None

            selected_discipline = Discipline.objects.get(id=discipline_id) if self._valid_org_id(discipline_id) else None
            selected_subdiscipline = SubDiscipline.objects.get(id=subdiscipline_id) if self._valid_org_id(subdiscipline_id) else None
            show_inactive_orgs = request.POST.get("show_inactive_orgs", None)

            return render(request, self.template, locals())


@login_required
@apply_perms
def search_sop_biennial_review(request, **kwargs):
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

    return render(request, 'main/search_sop_biennial_review.html', locals())


@login_required
@apply_perms
def result_search_sop_biennial_review(request, **kwargs):

    user = request.user
    the_count = 0
    lead_office_id = request.GET.get("office", None)

    if lead_office_id is not None:
        sop_biennial_SQL = (
            "select id, "
            "(select abbreviation from organization_office where id = office_id) as office, "
            "(select abbreviation from organization_lab where id = lab_id) as lab, "
            "(select abbreviation from organization_division where id = division_id) as division, "
            "(select abbreviation from organization_branch where id = branch_id) as branch, "
            "office_id, "
            "lab_id, "
            "division_id, "
            "branch_id, "
            "sop_number, "
            "previous_id, "
            "alt_id, "
            "full_title, "
            "(select the_name from sop_tab_soptab_status where id = sop_status_id) as sop_status, "
            "COALESCE(date_reviewed, date_approved) as sop_date, "
            "(select email from auth_user where id = sop_contact_id) as sop_contact, "
            "(select email from auth_user where id = approving_manager_id) as approving_manager, "
            "(select email from auth_user where id = approving_line_manager_id) as approving_line_manager, "
            "suspend_reminder, "
            "le.last_email_sent "
            "from sop_tab_soptab st "
            "left join (select soptab_id, max(date_email_sent) as last_email_sent from sop_tab_sopreminder "
            "group by soptab_id) le on (le.soptab_id = st.id) "
            "where "
            "sop_status_id in (select id from sop_tab_soptab_status where the_name in ('Active','Under Review')) "
            "and "
            "COALESCE(date_reviewed, date_approved) < (now() - INTERVAL '2 year')"
        )

        # return HttpResponse(baseSQL)

        lead_lab_id = request.GET.get("lab", None)
        lead_division_id = request.GET.get("division", None)
        lead_branch_id = request.GET.get("branch", None)

        ## Add criteria to baseSQL
        sop_biennial_criteria = ''
        if lead_office_id is not None and lead_office_id != '':
            sop_biennial_SQL += " and office_id = " + lead_office_id
            sop_biennial_criteria = "Lead Organization = " + str(Office.objects.get(id=lead_office_id)) + " and "

            if lead_lab_id is not None and lead_lab_id != '':
                sop_biennial_SQL += " and lab_id = " + lead_lab_id
                sop_biennial_criteria = "Lead Organization = " + str(Lab.objects.get(id=lead_lab_id)) + " and "

                if lead_division_id is not None and lead_division_id != '':
                    sop_biennial_SQL += " and division_id = " + lead_division_id
                    sop_biennial_criteria = "Lead Organization = " + \
                                            str(Division.objects.get(id=lead_division_id)) + " and "

                    if lead_branch_id is not None and lead_branch_id != '':
                        sop_biennial_SQL += " and branch_id = " + lead_branch_id
                        sop_biennial_criteria = "Lead Organization = " \
                                                + str(Branch.objects.get(id=lead_branch_id)) + " and "


        if 'contact_last' in request.GET:
            contact_last = request.GET['contact_last']
            if contact_last:
                sop_biennial_SQL += " and sop_contact_id in (select id from auth_user where upper(last_name) " \
                          "like upper('" + contact_last + "%%'))"
                sop_biennial_criteria += "SOP Contact Last Name starts with " + str(contact_last) + " and "

        if 'contact_first' in request.GET:
            contact_first = request.GET['contact_first']
            if contact_first:
                sop_biennial_SQL += " and sop_contact_id in (select id from auth_user where upper(first_name) " \
                          "like upper('" + contact_first + "%%'))"
                sop_biennial_criteria += "SOP Contact First Name starts with " + str(contact_first) + " and "

        if 'approving_manager_last' in request.GET:
            approving_manager_last = request.GET['approving_manager_last']
            if approving_manager_last:
                sop_biennial_SQL += " and approving_manager_id in (select id from auth_user where upper(last_name) " \
                          "like upper('" + approving_manager_last + "%%'))"
                sop_biennial_criteria += "Approving QA Manager Last Name starts with " \
                                         + str(approving_manager_last) + " and "

        if 'approving_manager_first' in request.GET:
            approving_manager_first = request.GET['approving_manager_first']
            if approving_manager_first:
                sop_biennial_SQL += " and approving_manager_id in (select id from auth_user where upper(first_name) " \
                          "like upper('" + approving_manager_first + "%%'))"
                sop_biennial_criteria += "Approving QA Manager First Name starts with " \
                                         + str(approving_manager_first) + " and "

        if 'approving_line_manager_last' in request.GET:
            approving_line_manager_last = request.GET['approving_line_manager_last']
            if approving_line_manager_last:
                sop_biennial_SQL += " and approving_line_manager_id in (select id from auth_user where upper(last_name) " \
                          "like upper('" + approving_line_manager_last + "%%'))"
                sop_biennial_criteria += "Approving Line Manager Last Name starts with " \
                                         + str(approving_line_manager_last) + " and "

        if 'approving_line_manager_first' in request.GET:
            approving_line_manager_first = request.GET['approving_line_manager_first']
            if approving_line_manager_first:
                sop_biennial_SQL += " and approving_line_manager_id in (select id from auth_user where upper(first_name) " \
                          "like upper('" + approving_line_manager_first + "%%'))"
                sop_biennial_criteria += "Approving Line Manager First Name = " \
                                         + str(approving_line_manager_first) + " and "

        sop_biennial_SQL += " order by sop_number"

        if sop_biennial_criteria != "":
            sop_biennial_criteria = sop_biennial_criteria[:-5]
        else:
            sop_biennial_criteria = "no criteria"

        objs = User.objects.raw(sop_biennial_SQL)
        # the_count = len(objs)   # len does not work for raw sql object

        for obj in objs:
            the_count += 1
            obj.curr_qams = get_qamanagers(obj.office_id, obj.lab_id, obj.division_id, obj.branch_id)

        query_show = sop_biennial_criteria




    # Check if user wants to export to Excel. Only do if there are results.
    if 'excel' in request.GET and the_count>0:
        excel = request.GET['excel']
        if excel == "Y":
            sops = objs
            #the_count = SOPTab.objects.filter(query).count()

            response = HttpResponse(content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=SOPsNeedingReview.xlsx'

            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})

            styles = {'datetime': xlwt.easyxf(num_format_str='yyyy-mm-dd hh:mm:ss'),
                      'date': xlwt.easyxf(num_format_str='yyyy-mm-dd'),
                      'time': xlwt.easyxf(num_format_str='hh:mm:ss'),
                      'default': xlwt.Style.default_style}

            worksheet = workbook.add_worksheet('Biennial SOP Reviews')
            label_format = workbook.add_format({'bold': True})
            section_format = workbook.add_format({'bold': True, 'font_color': '#337AB7'})
            row = 0

            worksheet.merge_range(row, 0, row, 6, "All SOPs Needing Biennial Reviews", section_format)

            row += 1
            today = datetime.now()
            worksheet.write(row, 0, "As of", label_format)
            worksheet.write(row, 1, str(today.date()))

            row += 2

            worksheet.write(row, 0, 'SOP Number', label_format)
            worksheet.write(row, 1, 'Previous ID', label_format)
            worksheet.write(row, 2, 'Alternate ID', label_format)
            worksheet.write(row, 3, 'Full Title', label_format)

            worksheet.write(row, 4, 'Lead Organization Office', label_format)
            worksheet.write(row, 5, 'Lead Organization Center/Office', label_format)
            worksheet.write(row, 6, 'Lead Organization Division', label_format)
            worksheet.write(row, 7, 'Lead Organization Branch', label_format)

            worksheet.write(row, 8, 'Status', label_format)
            worksheet.write(row, 9, 'Approval or Last Review Date', label_format)

            worksheet.write(row, 10, 'SOP Contact', label_format)
            worksheet.write(row, 11, 'Approving QA Manager', label_format)
            worksheet.write(row, 12, 'Approving Line Manager', label_format)

            worksheet.write(row, 13, "Suspend Reminder?", label_format)
            worksheet.write(row, 14, "Email Sent", label_format)


            for obj in sops:
                row += 1
                worksheet.write(row, 0, obj.sop_number)
                worksheet.write(row, 1, obj.previous_id)
                worksheet.write(row, 2, obj.alt_id)

                worksheet.write(row, 3, obj.full_title)

                if obj.office is not None:
                    worksheet.write(row, 4, obj.office)
                else:
                    worksheet.write(row, 4, '')

                if obj.lab is not None:
                    worksheet.write(row, 5, obj.lab)
                else:
                    worksheet.write(row, 5, '')

                if obj.division is not None:
                    worksheet.write(row, 6, obj.division)
                else:
                    worksheet.write(row, 6, '')

                if obj.branch is not None:
                    worksheet.write(row, 7, obj.branch)
                else:
                    worksheet.write(row, 7, '')

                if obj.sop_status is not None:
                    worksheet.write(row, 8, obj.sop_status)
                else:
                    worksheet.write(row, 8, '')

                if obj.sop_date:
                    worksheet.write(row, 9, str(obj.sop_date))
                else:
                    worksheet.write(row, 9, '')

                if obj.sop_contact is not None:
                    worksheet.write(row, 10, obj.sop_contact)
                else:
                    worksheet.write(row, 10, '')

                if obj.approving_manager is not None:
                    worksheet.write(row, 11, obj.approving_manager)
                else:
                    worksheet.write(row, 11, '')

                if obj.approving_line_manager is not None:
                    worksheet.write(row, 12, obj.approving_line_manager)
                else:
                    worksheet.write(row, 12, '')

                if obj.suspend_reminder:
                    worksheet.write(row, 13, str(obj.suspend_reminder))
                else:
                    worksheet.write(row, 13, '')

                if obj.last_email_sent:
                    worksheet.write(row, 14, str(obj.last_email_sent.date()))

            # Add a sheet with the query so user knows if these have been filtered by org and/or person.
            sheet1 = workbook.add_worksheet('Query')
            sheet1.write(1, 0, sop_biennial_criteria)

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            xlsx_data = output.read()
            response.write(xlsx_data)
            return response

    return render(request, 'list/list_biennial_sop_review.html', locals())


# obj_id - id of SOP to toggle flag for
# sop_biennial_SQL - SQL query to recreate search
# query_show - description of query to display again on refresh
@login_required
@apply_perms
def switch_sop_reminder_flag(request, obj_id, **kwargs):

    user = request.user
    soptab = get_object_or_404(SOPTab, id=obj_id)

    if soptab.suspend_reminder != "Y":
        soptab.suspend_reminder = "Y"
    else:
        soptab.suspend_reminder = "N"

    soptab.save()

    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer)

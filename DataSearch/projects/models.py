from accounts.models import *
from constants.models import *
from audits.models import *

import offices.models as om
import labs.models as lm
import divisions.models as dm
import branches.models as bm
import organization.models as org
from persons.models import *
from DataSearch import settings
import datetime

from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser

from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver

import rms.models as rms_models

from django.utils import timezone

def get_ed_storage_path(instance, filename):
    return '%s/projects/%s' %(instance.user.username, filename)
def get_ed2_storage_path(instance, filename):
    return '%s/projects/%s' %(instance.user.username, filename)

def get_log_storage_path(instance, filename):
    return '%s/project_logs/%s' %(instance.user.username, filename)
def get_log2_storage_path(instance, filename):
    return '%s/project_logs/%s' %(instance.user.username, filename)
def get_pdf_storage_path(instance, filename):
    return '%s/qa_reviews/%s' %(instance.user.username, filename)

def get_review_storage_path(instance, filename):
    return '%s/reviews/%s' %(instance.user.username, filename)
def get_review2_storage_path(instance, filename):
    return '%s/reviews/%s' %(instance.user.username, filename)

def get_project_attachment_storage_path(instance, filename):
    if instance.where_from == 'Project':
        return 'project/%s/%s' % (instance.project_id, filename)
    else:
        return "project/%s/log/%s/%s" % (instance.project_id, instance.project_log_id, filename)

class ProjectStatus(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number',]

    def __str__(self):
        return self.the_name or ''

class ProjectType(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class QappStatus(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class QaCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)
    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class Program(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)
    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class NRMRLQAPPRequirement(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.the_name or ''

class VehicleType(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)
    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class ExtramuralVehicle(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    institution_name = models.CharField(blank=True, null=True, max_length=255)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_number = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)
    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class ProjectCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)
    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class ProjectNumber(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_serial_number = models.IntegerField(null=True, blank=True)
    this_serial_number = models.IntegerField(null=True, blank=True)
    next_serial_number = models.IntegerField(null=True, blank=True)
    the_name = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self):
        return self.the_name or ''


class ParticipatingOrganization(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, upload_to=get_profile_photo_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    # legacy fields
    lab_old = models.ForeignKey(lm.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division_old = models.ForeignKey(dm.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch_old = models.ForeignKey(bm.Branch, on_delete=models.CASCADE, null=True, blank=True)

    last_name = models.CharField(blank=True, null=True, max_length=30)
    first_name = models.CharField(blank=True, null=True, max_length=30)
    telephone = models.CharField(blank=True, null=True, max_length=30)
    telephone_extension = models.CharField(blank=True, null=True, max_length=30)

    mail_to_name = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    mail_to_address = models.CharField(blank=True, null=True, max_length=255)
    mail_to_city = models.CharField(blank=True, null=True, max_length=255)
    mail_to_state = models.CharField(blank=True, null=True, max_length=255)
    mail_to_zipcode = models.CharField(blank=True, null=True, max_length=255)
    mail_to_mailstop = models.CharField(blank=True, null=True, max_length=255)
    mail_to_note = models.CharField(blank=True, null=True, max_length=255)

    company = models.CharField(blank=True, null=True, max_length=255)

    email_address_epa = models.CharField(blank=True, null=True, max_length=255)
    email_address_other = models.CharField(blank=True, null=True, max_length=255)

    agreement_number = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    agreement_title = models.CharField(blank=True, null=True, max_length=255, db_index=True)


    class Meta:
        ordering = ['company',]

    def __str__(self):
        #the_name = self.company
        return self.company or ''

class Project(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, upload_to=get_ed_storage_path)
    attachment_02 = models.FileField(null=True, blank=True, upload_to=get_ed2_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="project_user")

    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="project_person")
    # legacy fields
    office_old = models.ForeignKey(om.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab_old = models.ForeignKey(lm.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division_old = models.ForeignKey(dm.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch_old = models.ForeignKey(bm.Branch, on_delete=models.CASCADE, null=True, blank=True)
    person_old = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

    programs = models.ManyToManyField(Program, blank=True)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, blank=True)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, null=True, blank=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, null=True, blank=True)
    qapp_status = models.ForeignKey(QappStatus, on_delete=models.CASCADE, null=True, blank=True)
    restrict_qapp_files = models.BooleanField(blank=False, default=False)
    restrict_ext_package_files = models.BooleanField(blank=False, default=False)
    qa_category = models.ForeignKey(QaCategory, on_delete=models.CASCADE, null=True, blank=True)
    nrmrl_qapp_requirement = models.ManyToManyField(NRMRLQAPPRequirement, blank=True)

    extramural_vehicle = models.ForeignKey(ExtramuralVehicle, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)

    qa_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="project_qa_manager")
    previous_qams = models.ManyToManyField(User, related_name="previous_qams", blank=True)
    collaborators = models.ManyToManyField(User, related_name="project_collaborators", blank=True)
    # legacy field
    collaborators_old = models.ManyToManyField(Person, related_name='collaborators', blank=True)
    participating_organizations = models.ManyToManyField(ParticipatingOrganization, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    product = models.CharField(blank=True, null=True, max_length=255)
    title = models.TextField(blank=True, null=True, db_index=True)

    the_description = models.TextField(null=True, blank=True)

    weblink = models.CharField(blank=True, null=True, max_length=255)
    ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)

    qa_id = models.CharField(blank=True, null=False, unique=True, max_length=255)

    previous_id = models.CharField(blank=True, null=True, max_length=255)
    alt_id = models.CharField(blank=True, null=True, max_length=255)

    ord_rap = models.CharField(blank=True, null=True, max_length=255)
    ord_rap_project = models.CharField(blank=True, null=True, max_length=255)
    ord_rap_task = models.CharField(blank=True, null=True, max_length=255)
    ord_rap_number = models.CharField(blank=True, null=True, max_length=255)
    ord_rap_project_number = models.CharField(blank=True, null=True, max_length=255)
    ord_rap_task_number = models.CharField(blank=True, null=True, max_length=255)

    ace_rap_numbers = models.TextField(null=True, blank=True)
    css_rap_numbers = models.TextField(null=True, blank=True)
    sswr_rap_numbers = models.TextField(null=True, blank=True)
    hhra_rap_numbers = models.TextField(null=True, blank=True)
    hsrp_rap_numbers = models.TextField(null=True, blank=True)
    hsrp_rap_extensions = models.TextField(null=True, blank=True)
    shc_rap_numbers = models.TextField(null=True, blank=True)

    rap_program = models.ForeignKey(rms_models.Program, on_delete=models.CASCADE, blank= True, null= True, related_name= "rap_program_projects")
    rap_project = models.ForeignKey(rms_models.Project, on_delete=models.CASCADE, blank=True, null=True, related_name= "rap_project_projects")
    rap_task = models.ForeignKey(rms_models.Task, on_delete=models.CASCADE, blank=True, null=True, related_name= "rap_task_projects")

    qapp_approval_date = models.DateField(null=True, blank=True)
    last_qapp_review_date = models.DateField(null=True, blank=True)
    product_qa_approval_date = models.DateField(null=True, blank=True)
    date_project_identified = models.DateField(null=True, blank=True)
    omis_task_number = models.CharField(blank=True, null=True, max_length=255)

    vehicle_number = models.CharField(blank=True, null=True, max_length=255)
    institution_name = models.CharField(blank=True, null=True, max_length=255)
    qmp_required = models.CharField(blank=True, null=True, max_length=25, choices=YN_CHOICES)
    qmp_required_name = models.CharField(blank=True, null=True, max_length=255)
    qmp_approval_date = models.DateField(null=True, blank=True)

    public_or_private = models.CharField(blank=True, null=True, max_length=25, choices=PUBLIC_CHOICES)

    suspend_reminder = models.CharField(default='N', max_length=2, choices=YN_CHOICES)

    class Meta:
        ordering = ["qa_id",]

    def __str__(self):
        return self.title or ''

    def get_absolute_url(self):
        return reverse('projects.views.show_project', args=[str(self.id)])

    def warning_list(self):
        the_answer = ''
        if self.date_project_identified is not None and self.qapp_approval_date is not None:
            if self.date_project_identified < self.qapp_approval_date:
                the_answer = the_answer + "Date Project Identified is AFTER the QAPP Approval Date."

        if self.date_project_identified is not None and self.qmp_approval_date is not None:
            if self.date_project_identified < self.qmp_approval_date:
                the_answer = the_answer + "Date Project Identified is AFTER the QMP Approval Date."

        return the_answer

class Project_Orgs(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)
    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['project_id', ]

    def __str__(self):
        # Return the abbreviation for the lowest level of organization that is not empty.
        if self.branch is not None:
            return str(self.branch)
        if self.division is not None:
            return str(self.division)
        if self.lab is not None:
            return str(self.lab)

        return str(self.office)

class ProjectProjectCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    project_category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, null=True, blank=True)

    the_description = models.TextField(null=True, blank=True)

class ProjectLogType(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    abbreviation = models.CharField(blank=True, null=True, max_length=25)

    next_major_number = models.IntegerField(null=True, blank=True)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name',]

    def __str__(self):
        return self.the_name or ''

class ProductCategory(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=2, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.the_name or ''

class ReviewType(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    abbreviation = models.CharField(blank=True, null=True, max_length=25)

    next_major_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["the_name",]

    def __str__(self):
        return self.the_name or ''

class QAPPReview(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    date_email_sent = models.DateTimeField(default=timezone.now, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=False)
    to_email_list = models.TextField(blank=True, null=True, db_index=True)
    cc_email_list = models.TextField(blank=True, null=True, db_index=True)

class ProjectLog(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, upload_to=get_log_storage_path)
    attachment_02 = models.FileField(null=True, blank=True, upload_to=get_log2_storage_path)
    attachment_pdf = models.FileField(null=True, blank=True, upload_to=get_pdf_storage_path)

    date_review_requested = models.DateField(null=True, blank=True, db_index=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)
    # legacy fields
    division_old = models.ForeignKey(dm.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch_old = models.ForeignKey(bm.Branch, on_delete=models.CASCADE, null=True, blank=True)


    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    project_log_type = models.ForeignKey(ProjectLogType, on_delete=models.CASCADE, null=True, blank=False)
    #
    technical_lead = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projectlog_tech_lead')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projectlog_reviewer')
    # legacy fields
    technical_lead_old = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name='technical_lead')
    reviewer_old = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name='reviewer')
    audit_type = models.ForeignKey(AuditType, on_delete=models.CASCADE, null=True, blank=True)
    review_type = models.ForeignKey(ReviewType, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    title = models.TextField(blank=True, null=True, db_index=True)

    the_description = models.TextField(null=True, blank=True)

    weblink = models.CharField(blank=True, null=True, max_length=255)
    ordering = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=1)

    qa_id = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    qa_log_number = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    qa_log_number_last = models.CharField(blank=True, null=True, max_length=255)
    qa_log_number_x = models.IntegerField(null=True, blank=True)
    qa_log_number_y = models.IntegerField(null=True, blank=True)

    previous_id = models.CharField(blank=True, null=True, max_length=255)
    alt_id = models.CharField(blank=True, null=True, max_length=255)

    recommendation = models.TextField(null=True, blank=True)
    date_received = models.DateField(null=True, blank=True, db_index=True)
    date_reviewed = models.DateField(null=True, blank=True, db_index=True)
    date_approved = models.DateField(null=True, blank=True, db_index=True)

    lco_tracking_number = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    omis_task_number = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    qa_review_required = models.CharField(blank=True, null=True, max_length=5, choices=YN_CHOICES)
    qapp = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)

    organization = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    audit_location = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    audit_date = models.DateField(blank=True, null=True)

    software_status = models.CharField(blank=True, null=True, max_length=45, choices=STATUS_CHOICES)
    public_or_private = models.CharField(blank=True, null=True, max_length=25, choices=PUBLIC_CHOICES)

    number_of_finding = models.CharField(blank=True, null=True, max_length=25)
    is_finding_resolved = models.CharField(blank=True, null=True, max_length=25, choices=YN_CHOICES)
    the_finding = models.CharField(blank=True, null=True, max_length=255)

    auditor = models.CharField(blank=True, null=True, max_length=255, db_index=True)
    auditor_organization = models.CharField(blank=True, null=True, max_length=255, db_index=True)

    qa_review_date = models.DateField(blank=True, null=True, db_index=True)
    qa_review_email_list = models.TextField(blank=True, null=True, db_index=True)
    qa_review_distribution_list = models.ManyToManyField(User, related_name='qa_review_distribution_list', blank=True)
    qa_review_comment = models.TextField(blank=True, null=True, db_index=True)

    are_corrective_actions_completed = models.CharField(blank=True, null=True, max_length=25, choices=YNNA_CHOICES)
    date_audit_report_submitted = models.DateField(blank=True, null=True, db_index=True)
    date_audit_closed = models.DateField(blank=True, null=True, db_index=True)
    date_responses_received = models.DateField(null=True, blank=True, db_index=True)

    class Meta:
        ordering = ["qa_log_number",]

    def __str__(self):
        return self.qa_log_number or ''


class ProjectAttachment(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, max_length=255, upload_to=get_project_attachment_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    project_log = models.ForeignKey(ProjectLog, on_delete=models.CASCADE, null=True, blank=True)

    is_qapp_review_file = models.CharField(default='N', max_length=2, choices=YN_CHOICES)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    the_size = models.CharField(blank=True, null=True, max_length=255)
    where_from = models.CharField(blank=True, null=True, max_length=255)

    is_latest_qapp_doc = models.CharField(default='N', max_length=2, choices=YN_CHOICES)
    is_latest_qapp_pdf = models.CharField(default='N', max_length=2, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name',]

    def icon_to_use(self):
        if str(self.attachment).endswith('pdf'):
            icon_src = settings.STATIC_URL + "img/pdf-icon.jpg"
        elif str(self.attachment).endswith('xls'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('xlsx'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('doc'):
            icon_src = settings.STATIC_URL + "img/word.png"
        elif str(self.attachment).endswith('docx'):
            icon_src = settings.STATIC_URL + "img/docx.png"
        elif str(self.attachment).endswith('doc'):
            icon_src = settings.STATIC_URL + "img/docx.png"
        elif str(self.attachment).endswith('html'):
            icon_src = settings.STATIC_URL + "img/html.png"
        elif str(self.attachment).endswith('txt'):
            icon_src = settings.STATIC_URL + "img/txt.jpg"
        elif str(self.attachment).endswith('csv'):
            icon_src = settings.STATIC_URL + "img/csv.png"
        elif str(self.attachment).endswith('psd'):
            icon_src = settings.STATIC_URL + "img/psd.jpg"
        else:
            icon_src = settings.STATIC_URL + "uploads/" + str(self.attachment)
        return icon_src


class Project_update_history(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="projhist_users")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    date_qappreviewed = models.DateField(null=True, blank=True, db_index=True)
    projectlead = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projhist_lead')
    qa_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projhist_qa_manager')
    comments = models.TextField(null=True, blank=True)
    project_status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE, null=True, blank=True)
    qapp_status = models.ForeignKey(QappStatus, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['id', ]


class ProjectLog_update_history(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="projloghist_users")

    project_log = models.ForeignKey(ProjectLog, on_delete=models.CASCADE, null=True, blank=True)

    date_approved = models.DateField(null=True, blank=True, db_index=True)
    review_type = models.ForeignKey(ReviewType, on_delete=models.CASCADE, null=True, blank=True)
    technical_lead = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projloghist_lead')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='projloghist_reviewer')
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['id', ]


class QaReviewDistribution(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    project_log = models.ForeignKey(ProjectLog, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["modified",]

    def __str__(self):
        return self.the_name or ''

    def cst(self):
        return self.modified - datetime.timedelta(hours=5)

class ProjectRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment_pdf = models.FileField(null=True, blank=True, upload_to=get_pdf_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    technical_lead = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="projectrequest_tech_lead")
    technical_lead_old = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    project_log = models.ForeignKey(ProjectLog, on_delete=models.CASCADE, null=True, blank=True)
    project_log_type = models.ForeignKey(ProjectLogType, on_delete=models.CASCADE, null=True, blank=False)

    date_submitted = models.DateField(null=True, blank=True, db_index=True)
    product_title = models.TextField(null=True, blank=True, db_index=True)

    product_type_other = models.TextField(null=True, blank=True)

    date_review_requested_by = models.DateField(null=True, blank=True, db_index=True)
    was_qapp_required = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)
    was_qapp_prepared = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)

    project_qa_id = models.CharField(null=True, blank=True, max_length=45, db_index=True)
    project_approval_date = models.DateField(null=True, blank=True, db_index=True)

    qapp_status_explanation = models.TextField(null=True, blank=True)

    dqi_met = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)
    dqi_met_some = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)
    dqi_met_some_bad_data = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)
    dqi_na = models.CharField(null=True, blank=True, max_length=5, choices=YN_CHOICES)

    dqi_explanation = models.TextField(null=True, blank=True)

    electronic_signature = models.CharField(null=True, blank=True, max_length=45, db_index=True)
    date_electronic_signature = models.DateField(null=True, blank=True, db_index=True)
    electronic_signature_title = models.CharField(null=True, blank=True, max_length=45, db_index=True)

    email_list = models.TextField(null=True, blank=True)


@receiver(post_delete, sender=ProjectAttachment)
def photo_post_delete_handler(sender, **kwargs):
    pa = kwargs['instance']
    storage, path = pa.attachment.storage, pa.attachment.path
    storage.delete(path)


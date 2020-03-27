from django.db import models
import organization.models as org
from django.contrib.auth.models import User, AnonymousUser
import projects.models as proj
import datetime
from constants.models import *
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

def get_soptab_attachment_storage_path(instance, filename):
	return 'sop_tab/%s/%s' % (instance.soptab_id, filename)

class SOPTab_MuralType(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name', ]

    def __str__(self):
        return self.the_name or ''

class SOPTab_Type(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    class Meta:
        ordering = ['the_name', ]

    def __str__(self):
        return self.the_name or ''


class SOPTab_Status(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.the_name or ''

class Discipline(models.Model):
    discipline = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(null=True, blank=True)

    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.discipline or ''

class SubDiscipline(models.Model):
    subdiscipline = models.CharField(blank=False, max_length=255)
    abbreviation = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(null=True, blank=True)

    # parent Discipline
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, blank=False)

    is_active = models.CharField(blank=True, null=True, max_length=4, choices=YN_CHOICES)

    sort_number = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sort_number', ]

    def __str__(self):
        return self.subdiscipline or ''

class SOPTab(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="soptab_users")

    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    sop_number = models.CharField(blank=True, null=True, max_length=255)
    alt_id = models.CharField(blank=True, null=True, max_length=255)

    full_title = models.TextField(null=True, blank=True)
    sop_contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='soptab_contacts')
    mural_type = models.ForeignKey(SOPTab_MuralType, on_delete=models.CASCADE, null=True, blank=True)
    sop_type = models.ForeignKey(SOPTab_Type, on_delete=models.CASCADE, null=True, blank=True)
    approving_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='soptab_approvers')
    date_approved = models.DateField(null=True, blank=True, db_index=True)
    date_reviewed = models.DateField(null=True, blank=True, db_index=True)
    date_last_revision = models.DateField(null=True, blank=True, db_index=True)
    keywords = models.TextField(null=True, blank=True)

    sop_status = models.ForeignKey(SOPTab_Status, on_delete=models.CASCADE, null=True, blank=True)
    previous_id = models.CharField(blank=True, null=True, max_length=255)
    previous_base_number = models.CharField(blank=True, null=True, max_length=255)
    programs = models.ManyToManyField(proj.Program, blank=True)
    projects = models.ManyToManyField(proj.Project, blank=True)
    ## ORD organizations - custom m2m uses SOPTabOrgs intermediate model (table)
    participating_orgs = models.ManyToManyField(proj.ParticipatingOrganization, blank=True)

    approving_line_manager =models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='soptab_approving_line_managers')

    sop_review_email_list = models.TextField(blank=True, null=True, db_index=True)
    sop_review_distribution_list = models.ManyToManyField(User, related_name='soptabs_review_distribution_list', blank=True)

    the_description = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    related_sops = models.ManyToManyField("self", blank=True)

    date_effective = models.DateField(null=True, blank=True, db_index=True)

    sop_base_number = models.CharField(blank=True, null=True, max_length=255)
    sop_version = models.IntegerField(null=True, blank=True)
    sop_base_id = models.IntegerField(null=True, blank=True)

    # legacy or in case it might be needed in future
    sop_number_x = models.IntegerField(null=True, blank=True)
    sop_number_y = models.IntegerField(null=True, blank=True)

    suspend_reminder = models.CharField(default='N', max_length=4, choices=YN_CHOICES)

    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, null=True, blank=True)
    subdiscipline = models.ForeignKey(SubDiscipline, on_delete=models.CASCADE, null=True, blank=True)

    is_current = models.CharField(default='Y', max_length=4, choices=YN_CHOICES)


    class Meta:
        ordering = ['sop_base_id', 'sop_version']
        get_latest_by = 'sop_version'

    def __str__(self):
        return self.sop_number or ''

class SOPReminder(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    date_email_sent = models.DateTimeField(default=timezone.now, null=True, blank=True)
    soptab = models.ForeignKey(SOPTab, on_delete=models.CASCADE, null=True, blank=True)

    to_email_list = models.TextField(blank=True, null=True, db_index=True)
    cc_email_list = models.TextField(blank=True, null=True, db_index=True)

class SOPTabReviewDistribution(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    soptab = models.ForeignKey(SOPTab, on_delete=models.CASCADE, null=True, blank=True)

    the_name = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["modified",]

    def __str__(self):
        return self.the_name or ''

    def cst(self):
        return self.modified - datetime.timedelta(hours=5)


class SOPTab_Orgs(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)

    soptab = models.ForeignKey(SOPTab, on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(org.Office, on_delete=models.CASCADE, null=True, blank=True)
    lab = models.ForeignKey(org.Lab, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(org.Division, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(org.Branch, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['soptab_id', ]

    def __str__(self):
        # Return the abbreviation for the lowest level of organization that is not empty.
        if self.branch is not None:
            return str(self.branch)
        if self.division is not None:
            return str(self.division)
        if self.lab is not None:
            return str(self.lab)

        return str(self.office)

class SOPTabAttachment(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    attachment = models.FileField(null=True, blank=True, max_length=255,
                                  upload_to=get_soptab_attachment_storage_path)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    soptab = models.ForeignKey(SOPTab, on_delete=models.CASCADE, null=True, blank=True, related_name="soptab_attachments")

    include_in_email = models.CharField(default='N', max_length=4, choices=YN_CHOICES)
    is_review_file = models.CharField(default='N', max_length=4, choices=YN_CHOICES)
    is_latest_sop = models.CharField(default='N', max_length=4, choices=YN_CHOICES)

    the_name = models.CharField(blank=True, null=True, max_length=255)
    the_size = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        ordering = ['the_name', ]

    def icon_to_use(self):
        if str(self.attachment).endswith('pdf'):
            icon_src = settings.STATIC_URL + "img/pdf-icon.jpg"
        elif str(self.attachment).endswith('xls'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('xlsx'):
            icon_src = settings.STATIC_URL + "img/xlsx.jpg"
        elif str(self.attachment).endswith('doc'):
            icon_src = settings.STATIC_URL + "img/word.png"
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


class SOPTab_approval_history(models.Model):
    created = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified = models.DateTimeField(default=timezone.now, null=True, blank=True)
    created_by = models.CharField(blank=True, null=True, max_length=255)
    last_modified_by = models.CharField(blank=True, null=True, max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sophist_users")

    soptab = models.ForeignKey(SOPTab, on_delete=models.CASCADE, null=True, blank=True)

    date_reviewed = models.DateField(null=True, blank=True, db_index=True)
    sop_contact = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sophist_contacts')
    approving_manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sophist_approving_managers')
    comments = models.TextField(null=True, blank=True)
    sop_status = models.ForeignKey(SOPTab_Status, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ['id', ]

@receiver(post_delete, sender=SOPTabAttachment)
def photo_post_delete_handler(sender, **kwargs):
    pa = kwargs['instance']
    storage, path = pa.attachment.storage, pa.attachment.path
    storage.delete(path)
